from collections import defaultdict

from main.tokens.data import Token
from main.board.board import Board

class Sieciarze:
    def __init__(self, board : Board):
        self.board : Board = board
        # self.kwestia_sieciarzy()

    @classmethod
    def compute(cls, board):
        cls(board).kwestia_sieciarzy()

    def dfs1(self, akt):
        self.odw.add(akt)

        for i in self.graf_sieciarzy[akt]:
            if i not in self.odw:
                self.dfs1(i)

        self.kolejka.append(akt)

    def dfs2(self, akt, kolor):
        self.odw.add(akt)
        self.kolory[akt] = kolor

        for i in self.odwr_sieciarzy[akt]:
            if i not in self.odw:
                self.dfs2(i, kolor)

    def zbuduj_graf(self):
        self.graf_sieciarzy = defaultdict(list)
        self.odwr_sieciarzy = defaultdict(list)
        self.wszyscy_sieciarze = set()

        for x in range(self.board.width):
            for y in range(self.board.length):
                akt = self.board.get_token((x, y))
                if akt is None:
                    continue
                
                wires = akt.wire
                if len(wires) == 0:
                    continue

                self.wszyscy_sieciarze.add((x, y))
                self.graf_sieciarzy[(x, y)]
                self.odwr_sieciarzy[(x, y)]

                kierunki = wires

                for kier in kierunki:
                    nx, ny = self.board.go((x, y), kier)

                    print(f"Sieciarz ({x},{y}) frakcja {akt.faction} kierunek {kier} -> ({nx},{ny}), frakcja {self.board.get_token((nx, ny)).faction if self.board.get_token((nx, ny)) is not None else 'None'} is valid: {self.board.is_valid_target((nx, ny), akt.faction)}")

                    if not self.board.is_valid_target((nx, ny), akt.faction):
                        continue

                    cel = self.board.get_token((nx, ny))

                    if cel is None or not cel.can_wire():
                        continue

                    self.graf_sieciarzy[(x, y)].append((nx, ny))
                    self.odwr_sieciarzy[(nx, ny)].append((x, y))

    def policz_scc(self):
        self.kolejka = []
        self.odw = set()

        for siec in self.wszyscy_sieciarze:
            if siec not in self.odw:
                self.dfs1(siec)

        self.kolory = dict()
        self.odw = set()

        kolor = 0

        while self.kolejka:
            siec = self.kolejka.pop()

            if siec not in self.odw:
                self.dfs2(siec, kolor)
                kolor += 1

        self.ile_kolorow = kolor

        # print("Sieciarze, kolory:")
        # for siec in self.wszyscy_sieciarze:
        #     print(siec, "->", self.kolory[siec])


    def zbuduj_graf_scc(self):
        self.graf_scc = defaultdict(set)
        self.sieci_w_kolorze = defaultdict(list)
        self.stopien = defaultdict(int)

        for siec in self.wszyscy_sieciarze:
            kol1 = self.kolory[siec]

            self.sieci_w_kolorze[kol1].append(siec)

            for i in self.graf_sieciarzy[siec]:
                kol2 = self.kolory[i]

                if kol1 != kol2 and kol2 not in self.graf_scc[kol1]:
                    self.graf_scc[kol1].add(kol2)
                    self.stopien[kol2] += 1

        # print("Graf SCC:")
        # for kol in self.graf_scc:
        #     print(kol, "->", list(self.graf_scc[kol]))

        # print("Sieci w kolorze:")
        # for kol in self.sieci_w_kolorze:
        #     print(kol, "->", self.sieci_w_kolorze[kol])

    def rozpatrz_scc(self, kolor):
        wierzcholki = self.sieci_w_kolorze[kolor]
        zasiecowanie = dict()

        # print(wierzcholki, kolor, self.sieci_w_kolorze)

        for siec in wierzcholki:
            zasiecowanie[siec] = 0 # 0 - undefined; 1 - aktywny; 2 - zasieciowany

        for siec in wierzcholki:
            for napastnik in self.odwr_sieciarzy[siec]:
                if self.kolory[napastnik] == kolor:
                    continue

                if self.status_sieciarzy[napastnik] == 1:
                    zasiecowanie[siec] = 2
                    break

        zmiana = True

        while zmiana:
            zmiana = False

            for siec in wierzcholki:
                if zasiecowanie[siec] != 0:
                    continue

                ma_wewnetrznych_napastnikow = False
                czy_wszyscy_zasieciowani = True
                czy_ma_aktywnego = False

                for napastnik in self.odwr_sieciarzy[siec]:
                    if self.kolory[napastnik] != kolor:
                        continue

                    ma_wewnetrznych_napastnikow = True
                    stan = zasiecowanie[napastnik]

                    if stan == 1:
                        czy_ma_aktywnego = True

                    if stan != 2:
                        czy_wszyscy_zasieciowani = False

                if czy_ma_aktywnego:
                    zasiecowanie[siec] = 2
                    zmiana = True
                    continue

                if not ma_wewnetrznych_napastnikow:
                    zasiecowanie[siec] = 1
                    zmiana = True
                    continue

                if czy_wszyscy_zasieciowani:
                    zasiecowanie[siec] = 1
                    zmiana = True
                    continue

        for siec in wierzcholki:
            if zasiecowanie[siec] == 0:
                zasiecowanie[siec] = 1

        for siec in wierzcholki:
            self.status_sieciarzy[siec] = zasiecowanie[siec]

        # print(f"Rozpatrzono SCC {kolor}:")
        # for siec in wierzcholki:
        #     napis = "aktywny" if self.status_sieciarzy[siec] == 1 else "zasieciowany"
        #     print("   ", siec, "->", napis)

    def kwestia_sieciarzy(self):
        self.zbuduj_graf()
        self.policz_scc()
        self.zbuduj_graf_scc()

        self.status_sieciarzy = defaultdict(int)

        queue = []

        # print("\nStopien SCC:")
        # for kolor, st in self.stopien.items():
        #     print(f"{kolor} -> kolor {st}")
        # print("------\n")

        # print("kolory --->", self.kolory)

        for kolor in range(self.ile_kolorow):
            if self.stopien[kolor] == 0:
                queue.append(kolor)

        while len(queue) > 0:
            akt = queue.pop()
            self.rozpatrz_scc(akt)

            for i in self.graf_scc[akt]:
                self.stopien[i] -= 1

                if self.stopien[i] == 0:
                    queue.append(i)

        # print("Aktywnosc sieciarzy: ")        
        # for i, j in self.status_sieciarzy.items():
        #     print(i, "->", j)

        # return self.status_sieciarzy

        for i in range(self.board.width):
            for j in range(self.board.length):
                cel = self.board.get_token((i, j))
                
                if (cel != None):
                    cel.unwire()

        for i in self.status_sieciarzy:
            akt = self.board.get_token(i)
            
            if self.status_sieciarzy[i] != 1:
                akt.set_wire()    
                continue
                
            for kier in (akt.wire or []):
                nx, ny = self.board.go(i, kier)
                cel = self.board.get_token((nx, ny))

                if (not self.board.is_valid_target((nx, ny), akt.faction)) or cel.can_wire() == True:
                    continue

                cel.set_wire()

        self.status_sieciarzy = dict(self.status_sieciarzy)

        # print("--------------------------------------------\n")
