from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, WindowProperties

class MyApp(ShowBase):

    # def umiesc(self, x, z, obraz, ind):
    #     cm = CardMaker(ind)
    #     a = self.a
    #     a *= 0.5
    #     cm.setFrame(-a, a, -a, a)
    #     node = aspect2d.attachNewNode(cm.generate())
    #     node.setBin("fixed", 1)
    #     node.setDepthTest(False)
    #     node.setDepthWrite(False)
    #     node.setPos(x*self.getAspectRatio(), 0, z)
    #     node.setTexture(self.loader.loadTexture(obraz))
    #     node.setTransparency(TransparencyAttrib.MAlpha)
    #     node.setHpr(0, 0, 29.5)
    #     return node
    
    # def wyswietl(self, obj):
    #     cm = CardMaker(obj.id)
    #     cm.setFrame(-obj.szer/2, obj.szer/2, -obj.wys/2, obj.wys/2)
    #     node = aspect2d.attachNewNode(cm.generate())
    #     node.setBin("fixed", obj.warstwa)
    #     node.setDepthTest(False)
    #     node.setDepthWrite(False)
    #     node.setPos(obj.x*self.getAspectRatio(), 0 , obj.z)
    #     node.setTexture(self.loader.loadTexture(obj.imgPath))
    #     node.setTransparency(TransparencyAttrib.MAlpha)
    #     node.setHpr(0, 0, obj.rotacja)
    #     return node

    # def robhexa(self, x, z, sz):
    #     lines = LineSegs()
    #     lines.setThickness(sz)
    #     pier = math.sqrt(3)
    #     # lines.moveTo(0, 0, 0) 
    #     szer = (self.a*pier)/2
    #     z += self.a
    #     lines.moveTo(x, 0, z)
    #     x += szer
    #     z -= self.a/2
    #     lines.drawTo(x, 0, z)
    #     z -= self.a
    #     lines.drawTo(x, 0, z)
    #     z -= self.a/2
    #     x -= szer
    #     lines.drawTo(x, 0, z)
    #     x -= szer
    #     z += self.a/2
    #     lines.drawTo(x, 0, z)
    #     z+=self.a
    #     lines.drawTo(x, 0, z)
    #     x+=szer
    #     z+=self.a/2
    #     lines.drawTo(x, 0, z)
    #     node = lines.create()
    #     pole = aspect2d.attachNewNode(node)
    #     pole.setBin("fixed", 10)
    #     pole.setDepthTest(False)
    #     pole.setDepthWrite(False)
    #     return pole
    
    # def plansza(self, sz):
    #     lista = []
    #     pier = math.sqrt(3)
    #     for i in range(-3, 4, 3):
    #         for j in range(-1, 2, 1):
    #             lista.append([i*self.a, j*self.a*pier])
    #     lista.append([0, 2*self.a*pier])
    #     lista.append([0, (-2)*self.a*pier])
    #     for i in range(-1, 2, 2):
    #         for j in range(-2, 2, 1):
    #             if(j == 0):
    #                 j+=1
    #             lista.append([self.a*i*(3/2), self.a*pier*j+((pier*self.a)/2)])
    #     for i in range(len(lista)):
    #         self.pola.append(self.robhexa(lista[i][1], lista[i][0], sz))
    
    def __init__(self):
        super().__init__()

        # Hide default mouse
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)

        # --- 1. Create square in render2d ---
        cm = CardMaker("square")
        cm.setFrame(-0.2, 0.2, -0.2, 0.2)  # size

        self.square = aspect2d.attachNewNode(cm.generate())
        self.square.setPos(0, 0, 0)  # center of screen
        self.square.setColor(0, 0, 1, 1)  # blue

        # --- 2. Create mouse cursor (visual) ---
        cm2 = CardMaker("cursor")
        cm2.setFrame(-0.05, 0.05, -0.05, 0.05)

        self.cursor = aspect2d.attachNewNode(cm2.generate())
        self.cursor.setColor(1, 0, 0, 1)  # red
        
        # --- 3. Update loop ---
        self.taskMgr.add(self.update, "update")

    def update(self, task):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()

            # Move cursor
            skaluj = self.getAspectRatio()
            self.cursor.setPos(mpos.getX() * skaluj, 0, mpos.getY())

            # --- 4. Detect overlap ---
            if self.is_hovering(mpos):
                self.square.setColor(0, 1, 0, 1)  # green when hovered
            else:
                self.square.setColor(0, 0, 1, 1)  # blue otherwise

        return task.cont

    def is_hovering(self, mpos):
        # Square center
        sx = self.square.getX()* self.getAspectRatio()
        sz = self.square.getZ()
        # Half size (same as setFrame)
        size = 0.2

        return (
            abs(mpos.getX() - sx) < size and
            abs(mpos.getY() - sz) < size
        )

app = MyApp()
app.run()