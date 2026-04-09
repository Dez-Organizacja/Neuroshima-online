from plansza import *
from rysujhanda import *
from pomjson import *
from objekt import *
from zadajrany import *
from truewsp import *
import math

def stanplanszy(self):
    bok = 0.18
    self.wszystko = []
    # przes = (bok*math.sqrt(3)/2)*1.1
    przes = 0
    plansza(self, bok, przes)
    gracz = json["aktualna frakcja"]
    opponent = json["druga frakcja"]
    print(gracz, opponent)
    moja = []
    for y in range(5):
        curr = []
        for x in range(9):
            if json["board"][y][x] != "None":
                curr.append(obj(
                    getX(x, bok)+przes,
                    getY(y, bok),
                    json["board"][y][x]["frakcja"] + "/" + json["board"][y][x]["nazwa"] + ".png",
                    bok*math.sqrt(3),
                    bok*2,
                    1,
                    json["board"][y][x]["rotacja"]*60 + 30,
                    json["board"][y][x]["nazwa"],
                    self,
                    1,
                    "hex",
                    bok))
                zadajrany(self, getX(x, bok)+przes, getY(y, bok), json["board"][y][x]["rany"], bok)
                curr[-1].wyswietl(True)
            else:
                curr.append("None")
        moja.append(curr)
    rhand(self, -1, gracz, json["hand"][gracz], bok)
    rhand(self, 1, opponent, json["hand"][opponent], bok)
    for y in range(5):
        for x in range(9):
            if json["czyklikalne"]["board"][y][x] > 0:
                ter = obj(
                    getX(x, bok)+przes,
                    getY(y, bok),
                    "inne/podswietl.png",
                    bok*math.sqrt(3),
                    bok*2,
                    1,
                    30,
                    "podswietl",
                    self,
                    0.3,
                    "hex",
                    bok)
                ter.wyswietl(True)
    terhand = []
    for element in json["czyklikalne"]["hand"][gracz]:
        if element == 1:
            terhand.append("podswietl")
        else:
            terhand.append("None")
    rhand(self, -1, "inne", terhand, bok)
    terhand = []
    for element in json["czyklikalne"]["hand"][opponent]:
        if element == 1:
            terhand.append("podswietl")
        else:
            terhand.append("None")
    rhand(self, 1, "inne", terhand, bok)


            

    
