import math
from objekt import *

def plansza(app, bok, start):
    a = bok
    lista = []
    pier = math.sqrt(3)
    for i in range(-3, 4, 3):
        for j in range(-1, 2, 1):
            lista.append([i*a, j*a*pier+start])
    lista.append([0, 2*a*pier+start])
    lista.append([0, (-2)*a*pier+start])
    for i in range(-1, 2, 2):
        for j in range(-2, 2, 1):
            lista.append([a*i*(3/2), a*pier*j+((pier*a)/2)+start])
    for i in range(len(lista)):
        ter = obj(lista[i][1]*1.1, lista[i][0]*1.1, "inne/pole.png", a*2*math.sqrt(3)/2, a*2, 0, 30, "a.png", app, 1, "hex", a)
        ter.wyswietl(True)
        drugi = obj(lista[i][1]*1.1, lista[i][0]*1.1, "inne/obwod.png", (a*2*math.sqrt(3)/2)*1.17, a*2*1.17, 10, 30, "a.png", app, 1, "hex", a)
        drugi.wyswietl(True)
        app.pola.append(ter)
    