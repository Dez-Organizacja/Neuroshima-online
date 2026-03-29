from panda3d.core import LineSegs
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, TransparencyAttrib, NodePath, WindowProperties
import math 

class obj:
    def __init__(self, x, z, imgPath, wys, szer, warstwa, rotacja, id, app, trans, klasa, a):
        self.app = app
        self.x = x
        self.z = z
        self.imgPath = imgPath
        self.wys = wys
        self.szer = szer
        self.a = a
        self.id = id
        self.warstwa = warstwa
        self.rotacja = rotacja
        self.trans = trans
        self.klasa = klasa
    def wyswietl(self):
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
        return self.node
    def usun(self):
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


class MyApp(ShowBase):
    def plansza(self):
        lista = []
        pier = math.sqrt(3)
        for i in range(-3, 4, 3):
            for j in range(-1, 2, 1):
                lista.append([i*self.a, j*self.a*pier])
        lista.append([0, 2*self.a*pier])
        lista.append([0, (-2)*self.a*pier])
        for i in range(-1, 2, 2):
            for j in range(-2, 2, 1):
                lista.append([self.a*i*(3/2), self.a*pier*j+((pier*self.a)/2)])
        for i in range(len(lista)):
            ter = obj(lista[i][1]*1.1, lista[i][0]*1.1, "pole.png", self.a*2*math.sqrt(3)/2, self.a*2, 0, 30, "a.png", self, 1, "hex", self.a)
            ter.wyswietl()
            drugi = obj(lista[i][1]*1.1, lista[i][0]*1.1, "obwod2.png", (self.a*2*math.sqrt(3)/2)*1.17, self.a*2*1.17, 10, 30, "a.png", self, 1, "hex", self.a)
            drugi.wyswietl()
            self.pola.append(ter)
    
    def rdraw(self, g):
        for i in range(-1, 2, 1):
            ter = obj(g*4*self.a*self.getAspectRatio()*1.1, (3/2)*self.a*math.sqrt(3)*i*1.1, self.img[i+1], self.a*2*math.sqrt(3)/2, self.a*2, 1, 30, self.img[i+1], self, 1, "hex", self.a)
            ter.wyswietl()
            self.przesuwalne.append(ter)
            self.podswietlone[ter] = self.pusty

    def kursor(self):
        cm = CardMaker("kursor")
        cm.setFrame(-0.005, 0.005, -0.005, 0.005)
        self.kursor = aspect2d.attachNewNode(cm.generate())
        self.kursor.setColor(0, 0, 0, 1)
        self.kursor.setBin("fixed", 0)
    def klik(self):
        # print("CLICK")
        mpos = self.mouseWatcherNode.getMouse()
        if(self.klikniety.id == self.pusty.id):
            for element in self.przesuwalne:
                self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
                if(element.zawiera(self.kursor.getX(), self.kursor.getZ())):
                    self.klikniety = element
                    ter = obj(element.x, element.z, "podswietl.png", self.a*2*math.sqrt(3)/2, self.a*2, 2, 30, "podswietl.png", self, 0.3, "hex", self.a)
                    ter.wyswietl()
                    self.podswietlone[element] = ter
        else:
            self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
            for pole in self.pola:
                if(pole.zawiera(self.kursor.getX(), self.kursor.getZ())):
                    self.podswietlone[self.klikniety].usun()
                    self.podswietlone[self.klikniety] = self.pusty
                    self.klikniety.usun()
                    self.klikniety.x = pole.x
                    self.klikniety.z = pole.z
                    self.klikniety.wyswietl()
                    self.klikniety = self.pusty
                    
                    
                    break
    def upkursor(self, task):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            for element in self.przesuwalne:
                self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
                # if (self.zawiera(element) and self.podswietlone[element] == self.pusty):
                #     ter = obj(element.x, element.z, "podswietl.png", self.a*2*math.sqrt(3)/2, self.a*2, 2, 30, "podswietl.png", self, 0.3)
                #     ter.wyswietl()
                #     self.podswietlone[element] = ter
                #     # self.licznik+=1
                #     # print(self.licznik)
                # elif (not self.zawiera(element)) and self.podswietlone[element] != self.pusty:
                #     self.podswietlone[element].usun()
                #     self.podswietlone[element] = self.pusty
                # elif(self.podswietlone[element] != self.pusty):
                #     self.podswietlone[element].usun()
                #     self.podswietlone[element].x = element.x
                #     self.podswietlone[element].z = element.z
                #     self.podswietlone[element].wyswietl()

        return task.cont
    
    def __init__(self):
        super().__init__()
        # self.setBackgroundColor(0, 0, 0)
        self.a = 0.2
        # self.robhexa(0, 0, 2, 1)
        self.pola = []
        self.plansza()
        self.kursor()
        self.przesuwalne = []
        self.licznik = 0
        self.pusty = obj(0, 0, "test.png", 0, 0, 0, 0, "pusty", self, 0, "hex", self.a)
        self.klikniety = self.pusty
        self.podswietlone = dict()
        self.img = ["borgo/zwiadowca2.png", "borgo/zwiadowca.png", "test.png"]
        self.rdraw(-1)
        # self.taskMgr.add(self.upkursor, "upkursor")
        self.accept("mouse1", self.klik)

app = MyApp()
app.run()