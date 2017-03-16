from GapiMain import *

def Confirm():
    SetList((S.GetX(), S.GetY()), "System/ScreenSize")
    S.done = True
    Test.this.done = True

class S:
    done = False
    x, y = [0, 0]
    sx = (800, 960, 1024, 1280, 1600, 1920, 2560, 4096)
    sy = (600, 720, 768, 900, 1024, 1080, 1440, 2304)
    def GetX(nul=None):
        return (S.sx[S.x])

    def GetY(nul=None):
        return (S.sy[S.y])

    def X(w):
        if not((w == -1 and S.x == 0) or (w == 1 and S.x == len(S.sx)-1)):
            S.x += w

    def Y(w):
        if not((w == -1 and S.y == 0) or (w == 1 and S.y == len(S.sy)-1)):
            S.y += w
    

class Settings(dWorld):
    # Screen Vars
    this = None
    caption = "ScreenSizeSetter"
    size = (512, 256)
    exitKeys = {K.EXIT,}
    def __init__(self):
        Settings.this = self
        self.fps = 25

    def PostInit(self):
        self.wid = dLabel(pos=(0, 0), size=(128, 128),
                             col=C.BLACK, update=(S.GetX, None))
        self.hid = dLabel(pos=(512-128, 0), size=(128, 128),
                             col=C.BLACK, update=(S.GetY, None))
        lbl = dLabel(pos=(0, 128), size=(512, 128), col=C.BLACK,
                     text="Press Enter to test screen size.")
        incx = Change(pos=(256-64, 0),
                      texture=GetTexture("GraphicsSetter/Up"),
                      func=(S.X, 1))
        decx = Change(pos=(256-64, 64),
                      texture=GetTexture("GraphicsSetter/Down"),
                      func=(S.X, -1))
        incy = Change(pos=(256, 0),
                      texture=GetTexture("GraphicsSetter/Up"),
                      func=(S.Y, 1))
        decy = Change(pos=(256, 64),
                      texture=GetTexture("GraphicsSetter/Down"),
                      func=(S.Y, -1))

    def OnExit(self):
        S.done = True
        
    def OnKeyDown(self, kKey):
        if kKey == K.RETURN:
            self.done = True
            Run.Set(Test)

class Test(dWorld):
    this = None
    caption = "fullscreen"
    flags = pygame.FULLSCREEN
    exitKeys = {K.EXIT,}
    def __init__(self):
        Test.this = self
        self.fps = 25
        self.size = (S.GetX(), S.GetY())

    def PostInit(self):
        ConfirmWorking(pos=(0, 0),
                       texture=GetTexture("GraphicsSetter/Confirm"))

    def Update(self):
        if self.Time() >= 5:
            self.done = True
            S.done = False

class ConfirmWorking(Element):
    select = True
    def PostInit(self, *args, **kwargs):
        self.lbl = dLabel(pos=self.pos, size=self.size, col=C.BLACK,
                          text="Confirm Screen Size")

    def OnClick(self, mPos, mKey):
        if mKey == M.L_CLICK:
            Confirm()

class Change(Element):
    select = True
    def PostInit(self, *args, **kwargs):
        self.click = kwargs["func"]
        
    def OnClick(self, mPos, mKey):
        if mKey == M.L_CLICK:
            self.click[0](self.click[1])


while not S.done:
    Settings().Run()
