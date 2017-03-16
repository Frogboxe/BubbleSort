from time import clock as clk
from time import sleep
from os import path

def Test(*args):
    print(clk())

def TypeOf(text):
    if text == "int":
        return int
    elif text == "str":
        return str
    elif text == "flt":
        return float
    elif text == "Non":
        return Pass

"""
    FILE LOADING

"""

def RootCheck(root):
    return path.exists(root)

def LoadDict(root, types):
    if not RootCheck(root):
        return FileNotFound
    ret = dict()
    with open(root, "r") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            if line == "ENDKEK":
                return ret
            key, val = line.split(":")
            key, val = types[0](key), types[1](val)
            ret[key] = val
    return ret

def SaveDict(item, root):
    with open(root, "w") as f:
        for key, val in Range(item):
            f.write("{}:{}\n".format(key, val))
        f.write("ENDKEK")

def LoadSet(root):
    if not RootCheck(root):
        return FileNotFound
    ret = list()
    with open(root, "r") as f:
        curr = dict()
        for line in f.readlines():
            line = line.replace("\n", "")
            if line == "ENDOBJ":
                ret.append(curr)
                curr = dict()
            elif line == "ENDKEK":
                return ret
            else:
                cls, attr, val = (TypeOf(line.split(".")[0]),
                                  line.split(":")[0].split(".")[1],
                                  line.split(":")[1])
                curr[attr] = cls(val)

def SaveSet(root, items):
    with open(root, "w") as f:
        for item in items:
            for key, val in Range(item):
                f.write("{}.{}:{}\n".format(type(val).__name__[0:3], key, val))
            f.write("ENDOBJ\n")
        f.write("ENDKEK\n")
        
def LoadList(root, _type):
    if not RootCheck(root):
        return FileNotFound
    ret = list()
    with open(root, "r") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            if line == "ENDKEK":
                return ret
            ret.append(_type(line))

def SaveList(item, root):
    with open(root, "w") as f:
        for obj in item:
            f.write(str(obj)+"\n")
        f.write("ENDKEK")

def LoadString(root):
    if not RootCheck(root):
        return FileNotFound
    with open(root, "r") as f:
        ret = "\n".join(f.readlines())
    return ret

def SaveString(item, root):
    with open(root, "w") as f:
        for letter in item:
            f.write(letter)

"""
    ITERABLES

"""

def Exclude(_set, mapID, index=0):
    tmp = set()
    for item in _set:
        if item[index] == mapID:
            tmp.add(item)
    for item in tmp:
        _set.remove(item)
    return _set

def Range(x, y=None, z=False):
    if y == None:
        if isinstance(x, int):
            for i in range(x):
                yield i
        elif isinstance(x, dict):
            for key, val in zip(x, x.values()):
                yield key, val            
        else:
            for item, n in zip(x, range(len(x))):
                yield item, n
    elif not z:
        for ix in range(x):
            for iy in range(y):
                yield ix, iy
    elif z:
        for ix in range(x):
            for iy in range(y):
                yield ix, iy, (ix*x) + iy

"""
    KEYMAPPING

"""

class K:
    @staticmethod
    def DefineKeyMap():
        for char in Range(26):
            setattr(K, chr(char+97).upper(), char+97)
        for char in Range(12):
            setattr(K, "F"+str(char+1), char+282)

    @staticmethod
    def Populate(pop):
        K.MAP = pop
        for key, val in Range(pop):
            setattr(K, val, key)

    @staticmethod
    def IsNumber(kKey):
        kKey -= 48
        if kKey >= 0 and kKey <= 9:
            return True
        return False

    @staticmethod
    def Number(kKey):
        return kKey - 48     

"""
    MOUSEMAPPING

"""

class M:
    L_CLICK = 1
    M_CLICK = 2
    R_CLICK = 3
    ROLL_UP = 4
    ROLL_DN = 5


"""
    COLOURMAPPING

"""

def Col(col):
    col = int(col)
    r = col//(256**3)
    col -= r*(256**3)
    g = col//(256**2)
    col -= g*(256**2)
    b = col//(256)
    col -= b*(256)
    a = col
    return (r, g, b, a)

def ColToInt(col):
    _int = 0
    for i in range(4):
        _int += col[i]*(256**(3-i))
    return _int

class C:
    @staticmethod
    def Populate(pop):
        for key, val in Range(pop):
            setattr(C, key, val)

"""
    SKELLETON

"""

class GAPIError(Exception):
    pass

class skellyWorld:
    def OnKeyDown(self, kKey, kMod):
        pass

    def OnKeyUp(self, kKey):
        pass

    def OnFrame(self):
        pass

    def Update(self):
        pass

    def OnLogic(self):
        pass

    def PreInit(self):
        pass

    def PostInit(self):
        pass

class skellyElement:
    def OnClick(self, mPos, mKey):
        pass

    def Update(self):
        pass

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, texture):
        self._texture = texture
        self.OnChange()

class FileNotFound(Exception):
    pass

def Pass(*args):
    pass

"""
    IMPORT

"""

def IMPORT(keyMap, colMap):
    K.DefineKeyMap()
    K.Populate(keyMap)
    C.Populate(colMap)



