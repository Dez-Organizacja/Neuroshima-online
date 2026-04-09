from panda3d.core import LineSegs
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, TransparencyAttrib, NodePath, WindowProperties
from stanplanszy import *

class MyApp(ShowBase):
    # def kursor(self):
    #     cm = CardMaker("kursor")
    #     cm.setFrame(-0.005, 0.005, -0.005, 0.005)
    #     self.kursor = aspect2d.attachNewNode(cm.generate())
    #     self.kursor.setTransparency(TransparencyAttrib.MAlpha)
    #     self.kursor.setColor(0, 0, 0, 0)
    #     self.kursor.setBin("fixed", 0)
    def klik(self):
        # print("CLICK")
        mpos = self.mouseWatcherNode.getMouse()
        if(self.klikniety.id == self.pusty.id):
            for element in self.przesuwalne:
                if(element.zawiera(mpos.getX() * self.getAspectRatio(), mpos.getY())):
                    self.klikniety = element
                    ter = obj(element.x, element.z, "podswietl.png", self.a*2*math.sqrt(3)/2, self.a*2, 2, 30, "podswietl.png", self, 0.3, "hex", self.a)
                    ter.wyswietl()
                    self.podswietlone[element] = ter
                    break
        else:
            b = True
            # self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
            for pole in self.pola:
                if(pole.zawiera(mpos.getX() * self.getAspectRatio(), mpos.getY())):
                    b = False
                    self.podswietlone[self.klikniety].usun()
                    self.podswietlone[self.klikniety] = self.pusty
                    self.klikniety.usun()
                    self.klikniety.x = pole.x
                    self.klikniety.z = pole.z
                    self.klikniety.wyswietl()
                    self.klikniety = self.pusty
                    break
            if((b and self.podswietlone[self.klikniety] != self.pusty) and self.klikniety != self.pusty):
                self.podswietlone[self.klikniety].usun()
                self.podswietlone[self.klikniety] = self.pusty
                self.klikniety = self.pusty
    def obroc(self, kat):
        if(self.klikniety != self.pusty):
            self.klikniety.usun()
            self.klikniety.rotacja += 60*kat
            self.klikniety.wyswietl()
    def upkursor(self, task):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            for element in self.przesuwalne:
                self.kursor.setPos(mpos.getX() * self.getAspectRatio(), 0, mpos.getY())
                if (self.zawiera(element) and self.podswietlone[element] == self.pusty):
                    ter = obj(element.x, element.z, "podswietl.png", self.a*2*math.sqrt(3)/2, self.a*2, 2, 30, "podswietl.png", self, 0.3)
                    ter.wyswietl()
                    self.podswietlone[element] = ter
                    # self.licznik+=1
                    # print(self.licznik)
                elif (not self.zawiera(element)) and self.podswietlone[element] != self.pusty:
                    self.podswietlone[element].usun()
                    self.podswietlone[element] = self.pusty
                elif(self.podswietlone[element] != self.pusty):
                    self.podswietlone[element].usun()
                    self.podswietlone[element].x = element.x
                    self.podswietlone[element].z = element.z
                    self.podswietlone[element].wyswietl()

        return task.cont
    def skaluj(self, task):
        for element in self.przesuwalne:
            ter = element
            ter.usun(False)
            ter.wyswietl(False)
    def __init__(self):
        super().__init__()

        # self.music = self.loader.loadMusic("soundtracks/dziubdziub.mp3") #audio
        # self.music.setLoop(True) #zakomentuj jak nie chcesz
        # self.music.setVolume(0.0) #dodaj glosnosc jak chcesz super muzyke
        # self.music.play()
        self.bok = 0.18
        # self.setBackgroundColor(0, 0, 0)
        # self.a = 0.15
        # self.robhexa(0, 0, 2, 1)
        # self.wszystko = []
        self.pola = []
        # plansza(self, self.a)
        # self.kursor()
        self.przesuwalne = []
        # self.licznik = 0
        self.pusty = obj(0, 0, "test.png", 0, 0, 0, 0, "pusty", self, 0, "hex", self.bok)
        # self.klikniety = self.pusty
        # self.podswietlone = dict()
        # nowy = zamien(0, 0, "borgo", "granat", 0, 30, 0, 0, self, 1, 2)
        # nowy.wyswietl(True)
        # self.hand = ["borgo/zwiadowca.png", "borgo/zwiadowca.png", "test.png"]
        # rhand(self, "borgo", "borgo", self.hand, self.a)
        # # self.taskMgr.add(self.upkursor, "upkursor")
        # self.accept("mouse1", self.klik)
        # self.accept("arrow_left", self.obroc, [-1])
        # self.accept("arrow_right", self.obroc, [1])
        # self.accept("window-event", self.skaluj)
app = MyApp()
app.run()