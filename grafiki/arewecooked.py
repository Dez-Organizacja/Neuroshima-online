from panda3d.core import LineSegs
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, TransparencyAttrib, NodePath, WindowProperties
import math 

class MyApp(ShowBase):
    def umiesc(self, x, z, obraz, ind):
        cm = CardMaker(ind)
        a = self.a
        a *= 1.14
        cm.setFrame(-a, a, -a, a)
        node = aspect2d.attachNewNode(cm.generate())
        node.setBin("fixed", 0)
        node.setDepthTest(False)
        node.setDepthWrite(False)
        node.setPos(x*self.getAspectRatio(), 0, z)
        node.setTexture(self.loader.loadTexture(obraz))
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setHpr(0, 0, 29.5)
        return node
    def kursor(self):
        cm = CardMaker("cursor")
        cm.setFrame(-0.05, 0.05, -0.05, 0.05)
        self.kursor = aspect2d.attachNewNode(cm.generate())
        self.kursor.setColor(0, 1, 0, 1)

    def zawiera(self, element):
        ex = element.getX() * self.getAspectRatio()
        ez = element.getZ()
        mx = self.mouseWatcherNode.getMouse().getX() 
        mz = self.mouseWatcherNode.getMouse().getZ()
        return ((abs(mx-ex) < self.a) and (abs(mz-ez) > self.a))
    def rdraw(self, sz, g, img):
        for i in range(-1, 2, 1):
            self.przesuwalne.append(self.umiesc(g*4*self.a, (3/2)*self.a*math.sqrt(3)*i, img[i+1], img[i+1]))
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(0, 0, 0)
        self.a = 0.2
        sz = 5
        # props = WindowProperties()
        # self.robhexa(0, 0, 2, 1)
        # self.pola = []
        # self.plansza(sz)
        self.kursor()
        self.przesuwalne = []
        self.img = ["borgo/zwiadowca2.png", "borgo/zwiadowca.png", "borgo/medyk.png"]
        self.rdraw(sz, -1, self.img)
        # print(self.przesuwalne[0])
        # print('a')
        # self.przesuwalne.append(self.umiesc(0, 0, a, "borgo/zwiadowca2.png", "borgo/zwiadowca2.png"))
        # for i in range(len(self.przesuwalne)):
            # print(self.przesuwalne[i])
        # self.umiesc(0, 0,self.a, "borgo/zwiadowca2.png", "zwiadowca2")
        self.taskMgr.add(self.upkursor, "upkursor")

        

app = MyApp()
app.run()