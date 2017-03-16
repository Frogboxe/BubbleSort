import pygame

from collections import deque
from functools import lru_cache

from GapiExtend import *

def GetTexture(name):
    return pygame.image.load("Textures/"+name+".png").convert_alpha()

def SetTexture(name, surface):
    pygame.image.save(surface, "Textures/"+name+".png")

def GetDict(name, types):
    return LoadDict("Assets/"+name+".dict", types)

def SetDict(item, name):
    SaveDict(item, "Assets/"+name+".dict")

def GetSet(name):
    return LoadSet("Assets/"+name+".set")

def SetSet(obj, name):
    SaveSet("Assets/"+name+".set", obj)

def GetList(name, _type):
    return LoadList("Assets/"+name+".list", _type)

def SetList(item, name):
    SaveList(item, "Assets/"+name+".list")

class Run:
    obj = None
    @staticmethod
    def Set(cls):
        Run.obj = cls

    @staticmethod
    def Run():
        obj = Run.obj
        Run.obj = None
        obj().Run()


class dWorld(skellyWorld):
    # Engine Vars
    screenLayers = dict()
    screenStack = deque
    selectStack = deque
    mouseStack = deque
    flush = list()
    selected = None
    # Screen Vars
    fps = 25
    frame = 0
    screen = pygame.Surface
    caption = "pygameWindow"
    size = (256, 256)
    flags = 0
    done = False
    bg = "Default/Background"
    IMPORT(keyMap=GetDict("System/KeyMappings", (int, str)),
           colMap=GetDict("System/ColMappings", (str, Col)))
    def OnExit(self):
        pass

    def OnClick(self, mPos, mKey):
        self.EngineClick(mPos, mKey)
        
    def OnMouseUp(self, mPos, mKey):
        if dWorld.selected != None and mKey == M.L_CLICK:
            self.selected.Deselect()
            dWorld.selected = None
    
    def OnFlush(self):
        for item in self.flush:
            if item[1] == "l":
                getattr(self, item[0]).append(item[2])
            elif item[1] == "r":
                getattr(self, item[0]).appendleft(item[2])
            else:
                raise GAPIError("""Cannot flush with
                                direction {}"""
                                .format(item[2]))
        dWorld.flush = list()
        
    def EngineClick(self, mPos, mKey):
        self.selectStack = dWorld.IterStack(self.selectStack,
                                            "select",
                                            "RawClick",
                                            mPos, mKey)

    def CheckForExit(self, kKey):
        for key in self.exitKeys:
            if int(key) == int(kKey):
                self.done = True

    def Blit(self):
        self.screenStack = dWorld.IterStack(self.screenStack,
                                            "render", "Draw")

    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                self.OnKeyDown(event.key, pygame.key.get_mods())
                self.CheckForExit(event.key)
            elif event.type == pygame.KEYUP:
                self.OnKeyUp(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.OnClick(pygame.mouse.get_pos(),
                             event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.OnMouseUp(pygame.mouse.get_pos(),
                               event.button)

    def Init(self):
        self.PreInit()
        self.screenStack = deque()
        self.selectStack = deque()
        self.mouseStack = deque()
        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.init()
        pygame.display.init()
        Element.surface = self.screen
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(GetTexture("Default/Icon32"))
        pygame.font.init()

    def Run(self):
        self.Init()
        clock = pygame.time.Clock()
        Element((0, 0), GetTexture(self.bg))
        self.PostInit()
        while True:
            clock.tick(self.fps)
            self.OnFlush()
            self.Blit()
            self.Events()
            self.OnFrame()
            self.Update()
            dWorld.Flip()
            self.frame += 1
            if self.done:
                self.OnExit()
                pygame.display.quit()
                if Run.obj != None:
                    Run.Run()
                break

    def Clk(self):
        return self.frame / self.fps

    def Time(self):
        return self.frame // self.fps

    @staticmethod
    def Flip():
        pygame.display.flip()

    @staticmethod
    def IterStack(stack, attr, func, *args):
        n = 0
        while True:
            try:
                element = stack[n]
                element.Update()
                if getattr(element, attr):
                    getattr(element, func)(*args)
                if element.KILL_ME:
                    stack.remove(element)
                    n -= 1
                n += 1
            except IndexError:
                break
        return stack

    @staticmethod
    def MousePos():
        return pygame.mouse.get_pos()

class Element(skellyElement):
    KILL_ME = False
    surface = pygame.Surface
    pos = tuple
    size = tuple
    _texture = pygame.Surface
    points = tuple
    render = True
    select = False
    mouse = False
    def __init__(self, pos, texture, *args, **kwargs):
        self.pos = pos
        self.texture = texture
        self.Init()
        self.PostInit(*args, **kwargs)

    def PostInit(self, *args, **kwargs):
        pass

    def RawClick(self, mPos, mKey):
        if self.ThisInside(mPos):
            self.OnClick(mPos, mKey)

    def ThisInside(self, oPos):
        if oPos[0] > self.pos[0] and oPos[0] < self.pos[0] + self.size[0]:
            if oPos[1] > self.pos[1] and oPos[1] < self.pos[1] + self.size[1]:
                return True
        return False

    def Init(self):
        self.OnChange()
        dWorld.flush.append(("screenStack", "l", self))
        if self.select:
            dWorld.flush.append(("selectStack", "r", self))
        if self.mouse:
            dWorld.flush.append(("mouseStack", "r", self))

    def OnChange(self):
        self.size = self.texture.get_size()

    def Draw(self):
        Element.surface.blit(self.texture, self.pos)

    def KillThis(self):
        self.KILL_ME = True

    @staticmethod
    def getSurface(size, col):
        surf = pygame.Surface(size)
        surf.fill(col)
        surf = surf.convert()
        return surf

    @staticmethod
    def getClear(size):
        surf = pygame.Surface(size, pygame.SRCALPHA, 32)
        surf = surf.convert_alpha()
        return surf

class Mapping(Element):
    mapping = set()
    size = tuple()
    def __init__(self, size):
        self.size = size

    def AddTexture(self, mapID, pos, texture):
        self.mapping.add((mapID, pos, texture))

    def RemoveTexture(self, mapID):
        self.mapping = Exclude(_set=self.mapping,
                               mapID=mapID, index=0)

    def Refresh(self):
        surface = Element.getSurface(self.size, (0, 0, 0, 0))
        for item in self.mapping:
            surface.blit(item[2], item[1])
        self.texture = surface

class dScrollBar(Element):
    select = True
    held = False
    def __init__(self, bE, startPos, texture):
        self.host = bE
        self.pos = (bE.pos[0]+startPos, bE.pos[1])
        self.min = bE.pos[0]
        self.texture = texture
        self.Init()
        self.max = bE.pos[0] + bE.size[0] - self.size[0]
        self.range = self.max - self.min
        self.val = startPos / self.range

    def OnClick(self, mPos, mKey):
        if mKey == M.L_CLICK:
            dWorld.selected = self
            self.held = True
            self.comp = mPos[0]

    def Update(self):
        if self.held:
            self.comp = dWorld.MousePos()[0]-self.size[0]//2 - self.min
            if self.comp > self.max:
                self.comp = self.max
            elif self.comp < self.min:
                self.comp = self.min
            self.pos = (self.comp, self.pos[1])
            self.val = (self.comp - self.min) / self.range

    def Deselect(self):
        self.held = False

    def GetVal(self, nul):
        return self.val

class dLabel(Element):
    pygame.font.init()
    Element.font = pygame.font.SysFont("default", 24)
    text = ""
    def __init__(self, pos, size, col, text=None, update=(Pass, None)):
        self.pos = pos
        self.col = col
        self.update = update
        self.texture = Element.getClear(size)
        self.Init()
        if text != None:
            self.Set(text)

    def Set(self, text):
        render = dLabel.RenderLabel(text, self.col)
        renderSize = render.get_size()
        self.texture.blit(render, (self.size[0]//2
                              -renderSize[0]//2,
                              self.size[1]//2
                              -renderSize[1]//2))

    @staticmethod
    @lru_cache(1024)
    def RenderLabel(text, col):
        return Element.font.render(text, 1, col)

    def Update(self):
        text = str(self.update[0](self.update[1]))
        if text != self.text and text != "None":
            if text[0:2] == "./": text = text[1::]
            texture = Element.getClear(self.size)
            render = dLabel.RenderLabel(text, self.col)
            renderSize = render.get_size()
            texture.blit(render, (self.size[0]//2
                                  -renderSize[0]//2,
                                  self.size[1]//2
                                  -renderSize[1]//2))
            self.texture = texture
            self.text = text












