from panda3d.core import CardMaker, TransparencyAttrib, NodePath, WindowProperties
import math
class obj:
    def __init__(self, x, z, imgPath, wys, szer, warstwa, rotacja, id, app, trans, klasa, a):
        self.app = app
        self.x = x
        self.imgPath = imgPath
        self.z = z
        self.wys = wys
        self.szer = szer
        self.a = a
        self.id = id
        self.warstwa = warstwa
        self.rotacja = rotacja
        self.trans = trans
        self.klasa = klasa
    def wyswietl(self, per):
        cm = CardMaker(self.id)
        cm.setFrame(-self.szer/2, self.szer/2, -self.wys/2, self.wys/2,)
        self.node = aspect2d.attachNewNode(cm.generate())
        self.node.setBin("fixed", self.warstwa)
        self.node.setDepthTest(False)
        self.node.setDepthWrite(False)
        self.node.setPos(self.x, 0, self.z)
        self.node.setTexture(self.app.loader.loadTexture(self.imgPath))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        self.node.setColor(1, 1, 1, self.trans)
        self.node.setHpr(0, 0, self.rotacja)
        if(per):
            self.app.wszystko.append(self)
        return self.node
    def usun(self, per):
        if(per):
            self.app.wszystko.remove(self)
        self.node.removeNode()
    def zawiera(self, kx, kz):
        if self.klasa == "hex":
            stanx = abs(kx - self.x)
            stanz = abs(kz - self.z)
            w = math.sqrt(3) * self.a/2
            if stanz > self.a:
                return False
            if stanx > w:
                return False
            if stanx > math.sqrt(3) * (self.a - stanz):
                return False
            return True
        else:
            return ((abs(kx - self.x) < self.a) and (abs(kz - self.z) < self.a))