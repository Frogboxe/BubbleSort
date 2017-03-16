from GapiMain import *
from collections import deque # deque = double ended queue, a built-in with
							  # VERY fast insertion speeds

class World(dWorld):
	"""
	World object. Derived from dWorld object which handles all the graphics
	back end behind the screen. 
	"""
    auto = False # Automatically run animation
    comps = 0
    swaps = 0
    LIST = [2, 8, 5, 7, 3, 2] # Numbers to be Bubble sorted
    dDone = False
    n = None
    # Screen Variables (Do not change)
    this = None
    caption = "BubbleSort"
    size = (512, 256)
    exitKeys = {K.EXIT,}
    flags = 0
    def __init__(self):
        World.this = self
        self.fps = 25

    def PostInit(self):
        self.sort = BubbleSort(World.LIST) # Create a sorter
        self.list = World.LIST # Set-up the list
        for i, n in Range(self.list):
            self.list[n] = Bubble(n, i) # Convert list into Bubbles
        dLabel(pos=(0, 192), size=(128, 64), col=C.BLACK,
               update=(self.GetComps, None))
        dLabel(pos=(128, 192), size=(128, 64), col=C.BLACK,
               update=(self.GetSwaps, None))

    def Update(self):
		""" Method called every frame """
        if self.n != None:
            self.Advance(self.list[self.n], self.la, -1)
            self.Advance(self.list[self.n+1], self.lb, 1)
        if self.auto:
            if self.n == None:
                self.comps += 1
                s = self.sort.Next()
                if not s[0]:
                    self.dDone = True
                if s[2] == None:
                    pass
                else:
                    self.swaps += 1
                    self.n = s[2]
                    self.la = Lerp()
                    self.lb = Lerp()
            return

    def OnKeyDown(self, kKey, kMod):
        if not self.dDone and kKey == K.RETURN and self.n == None:
            self.comps += 1
            s = self.sort.Next()
            if not s[0]:
                self.dDone = True
            if s[2] == None:
                pass
            else:
                self.swaps += 1
                self.n = s[2]
                self.la = Lerp()
                self.lb = Lerp()
        elif not self.dDone and kKey == K.SPACE and self.n == None:
            self.auto = True
        elif self.n != None:
            self.la.DONE()
            self.lb.DONE()

    def Advance(self, obj, lerp, di):
        l = lerp()
        if (di == 1) and (not l[0]):
            self.n = None
            return
        x, y = obj.pos
        x += 2 * di
        y = int((1-l[1]) * di * 64)+64
        obj.pos = (x, y)

    def EndLine(self):
        self.nl = True

    def Move(self):
        self.nl = False

    def GetComps(self, *args):
        return "C: "+str(self.comps)

    def GetSwaps(self, *args):
        return "S: "+str(self.swaps)
    
class Done(Element):
    select = True
    def __init__(self, *args, **kwargs):
        super(Done, self).__init__(*args, **kwargs)

    def OnClick(self, mPos, mKey):
        World.this.done = True
    
class Bubble(dLabel):
    def __init__(self, n, i):
        super(Bubble, self).__init__(pos=(n*64, 64), size=(64, 64),
                                     col=C.BLACK, text=str(i))
        self.i = i
        self.n = n

    def __gt__(self, ot):
        return self.i > ot.i

    def __repr__(self): # DEBUG METHOD
        return str(self.i)

class BubbleSort: # Bubble sorter
    def __init__(self, _list):
        self.list = _list
        self.i = 0
        self.m = len(_list)

    def Next(self): # Step-by-step Sorting (one comparison per call).
        swap = None
        if self.i+1 != self.m:
            if self.list[self.i] > self.list[self.i+1]:
                swap = self.Swap()
            self.i += 1
        if self.i+1 == self.m and self.m != 2:
            self.i = 0
            self.m -= 1
        elif self.m == 2:
            World.this.auto = False
            print(self.list)
            Done(pos=(512-64, 0), texture=GetTexture("BubbleSort/Done"))
            return (False, self.list, swap)
        else:
            pass #Last in line
        return (True, self.list, swap)

    def Swap(self):
        tmp = self.list[self.i]
        self.list[self.i] = self.list[self.i+1]
        self.list[self.i+1] = tmp
        return self.i

class Lerp: # Hard-coded graph generator for smooth movement
    done = False
    def __init__(self):
        self.x = -1

    def __call__(self):
        if self.done:
            return (False, 1)
        self.x += 1/16
        if self.x != 1:
            return (True, self.x ** 2)
        return (False, 1)

    def DONE(self):
        self.done = True

World().Run()
   
