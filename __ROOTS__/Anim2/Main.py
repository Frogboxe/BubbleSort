from GapiMain import *
from collections import deque
from copy import copy

class World(dWorld):
    LIST = [2, 8, 5, 7, 3]
    dDone = False
    n = None
    # Screen Vars
    this = None
    caption = "default"
    size = (512, 192)
    exitKeys = {K.EXIT,}
    def __init__(self):
        World.this = self
        self.fps = 25

    def PostInit(self):
        self.sort = BubbleSort(World.LIST)
        self.list = World.LIST
        for i, n in Range(self.list):
            self.list[n] = Bubble(n, i)

    def Update(self):
        if self.n != None:
            self.Advance(self.list[self.n], self.la, 1)
            self.Advance(self.list[self.n+1], self.lb, -1)
        

    def OnKeyDown(self, kKey, kMod):
        print(self.list)
        if not self.dDone and kKey == K.RETURN:
            s = self.sort.Next()
            print(s)
            if not s[0]:
                self.dDone = True
            if s[2] == None:
                self.NoChange()
            else:
                self.n = s[2]
                self.la = Lerp()
                self.lb = Lerp()

    def Advance(self, obj, lerp, di):
        l = lerp()
        if (di == -1) and (not l[0]):
            self.n = None
            return
        x, y = obj.pos
        x += 1
        y = int(l[1] * di * 64)
        obj.pos = (x, y)        

    def NoChange(self):
        print("no change occured")
            
            
            

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

class BubbleSort:
    def __init__(self, _list):
        self.list = _list
        self.i = 0
        self.m = len(_list)

    def Next(self):
        swap = None
        if self.i+1 != self.m:
            if self.list[self.i] > self.list[self.i+1]:
                print(self.list)
                swap = self.Swap()
            self.i += 1
        if self.i+1 == self.m and self.m != 2:
            self.i = 0
            self.m -= 1
        elif self.m == 2:
            return (False, self.list, swap)
        else:
            return (True, self.list, swap)
        return (True, self.list, swap)

    def Swap(self):
        tmp = self.list[self.i]
        self.list[self.i] = self.list[self.i+1]
        self.list[self.i+1] = tmp
        return self.i

class Lerp:
    def __init__(self):
        self.x = -1

    def __call__(self):
        self.x += 1/32
        if self.x != 1:
            return (True, self.x ** 2)
        return (False, 1)

n="""
sort = BubbleSort([5, 6, 3, 5])
while True:
    s = sort()
    print(s[1])
    if not s[0]:
        break
""" 

World().Run()







if __name__ == "__main__":
    pass
    
