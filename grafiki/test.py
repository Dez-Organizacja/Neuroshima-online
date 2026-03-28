from panda3d.core import LineSegs
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, TransparencyAttrib, NodePath, WindowProperties
import math 

class obj:
    def __init__(self, x, z, imgPath, wys, szer, warstwa, rotacja, id, app):
        self.app = app
        self.x = x*self.app.getAspectRatio()
        self.z = z
        self.imgPath = imgPath
        self.wys = wys
        self.szer = szer
        self.id = id
        self.warstwa = warstwa
        self.rotacja = rotacja
    def wyswietl(self):
        cm = CardMaker(self.id)
        cm.setFrame(-self.wys/2, self.wys/2, -self.szer/2, self.szer/2)
        self.node = aspect2d.attachNewNode(cm.generate())
        self.node.setBin("fixed", self.warstwa)
        self.node.setDepthTest(False)
        self.node.setDepthWrite(False)
        self.node.setPos(self.x, 0, self.z)
        self.node.setTexture(self.app.loader.loadTexture(self.imgPath))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        self.node.setHpr(0, 0, self.rotacja)
        return self.node
    def usun(self):
        self.node.removeNode()


class MyApp(ShowBase):

    def robhexa(self, x, z, sz):
        lines = LineSegs()
        lines.setThickness(sz)
        pier = math.sqrt(3)
        # lines.moveTo(0, 0, 0) 
        szer = (self.a*pier)/2
        z += self.a
        lines.moveTo(x, 0, z)
        x += szer
        z -= self.a/2
        lines.drawTo(x, 0, z)
        z -= self.a
        lines.drawTo(x, 0, z)
        z -= self.a/2
        x -= szer
        lines.drawTo(x, 0, z)
        x -= szer
        z += self.a/2
        lines.drawTo(x, 0, z)
        z+=self.a
        lines.drawTo(x, 0, z)
        x+=szer
        z+=self.a/2
        lines.drawTo(x, 0, z)
        node = lines.create()
        pole = aspect2d.attachNewNode(node)
        pole.setBin("fixed", 10)
        pole.setDepthTest(False)
        pole.setDepthWrite(False)
        return pole
    
    def plansza(self, sz):
        lista = []
        pier = math.sqrt(3)
        for i in range(-3, 4, 3):
            for j in range(-1, 2, 1):
                lista.append([i*self.a, j*self.a*pier])
        lista.append([0, 2*self.a*pier])
        lista.append([0, (-2)*self.a*pier])
        for i in range(-1, 2, 2):
            for j in range(-2, 2, 1):
                if(j == 0):
                    j+=1
                lista.append([self.a*i*(3/2), self.a*pier*j+((pier*self.a)/2)])
        for i in range(len(lista)):
            self.pola.append(self.robhexa(lista[i][1], lista[i][0], sz))
    
    def rdraw(self, sz, g):
        for i in range(-1, 2, 1):
            ter = obj(g*4*self.a, (3/2)*self.a*math.sqrt(3)*i, self.img[i+1], self.a*2, self.a*2, 1, 0, self.img[i+1], self)
            ter.wyswietl()
            self.przesuwalne.append(ter)

    def kursor(self):
        cm = CardMaker("kursor")
        cm.setFrame(-0.05, 0.05, -0.05, 0.05)
        self.kursor = aspect2d.attachNewNode(cm.generate())
        self.kursor.setColor(0, 0, 0, 1)
        self.kursor.setBin("fixed", 0)

    def zawiera(self, element):
        ex = element.x
        ez = element.z
        mx = self.kursor.getX() 
        mz = self.kursor.getZ()
        return ((abs(mx-ex) < self.a) and (abs(mz-ez) < self.a))
    
    def klik(self):
        print("CLICK")
        mpos = self.mouseWatcherNode.getMouse()
        for element in self.przesuwalne:
            self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
            if self.zawiera(element):
                self.licznik+=1
                print(str(element.id) + " " + str(self.licznik))
    def upkursor(self, task):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            for element in self.przesuwalne:
                self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
                if self.zawiera(element):
                    self.licznik+=1
                    print(self.licznik)
        return task.cont
    
    def __init__(self):
        super().__init__()
        # self.setBackgroundColor(0, 0, 0)
        self.a = 0.2
        sz = 5
        props = WindowProperties()
        # self.robhexa(0, 0, 2, 1)
        self.pola = []
        # self.plansza(sz)
        self.kursor()
        self.przesuwalne = []
        self.licznik = 0
        self.img = ["borgo/zwiadowca2.png", "borgo/zwiadowca.png", "test.png"]
        self.rdraw(sz, -1)
        # print(self.przesuwalne[0])
        # nowy = obj(1, 1, "borgo/zwiadowca.png", 1, 1, 1, 0, "borgo/zwiadowca.png", self)
        # print(nowy.x)
        # self.przesuwalne.append(self.umiesc(0, 0, a, "borgo/zwiadowca2.png", "borgo/zwiadowca2.png"))
        # for i in range(len(self.przesuwalne)):
            # print(self.przesuwalne[i])
        # self.umiesc(0, 0,self.a, "borgo/zwiadowca2.png", "zwiadowca2")
        # self.taskMgr.add(self.upkursor, "upkursor")
        self.accept("mouse1", self.klik)

app = MyApp()
app.run()