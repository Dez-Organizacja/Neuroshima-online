from collections import defaultdict
from zeton import Zeton

class Board:
    def __init__(self):
        self.length = 9
        self.width = 5
        self.rotation_phase = False
        self.board = [[None] * self.length for i in range(self.width)]
        self.available_hexs = [[False] * self.length for i in range(self.width)]
        self.max_inicjatywa = 10

        self.roza = {
            0 : {"x" : -1, "y" : 1},
            1 : {"x" : 0, "y" : 2},
            2 : {"x" : 1, "y" : 1},
            3 : {"x" : 1, "y" : -1},
            4 : {"x" : 0, "y" : -2},
            5 : {"x" : -1, "y" : -1},
        }

    def postaw_zeton(self, x, y, zeton):
        self.board[x][y] = Zeton(x, y, zeton)
        # self.rotation_phase = True

    def rotate(self, x, y, rotacja):
        self.board[x][y].rotate(rotacja)

    def get_name(self, x, y):
        if(self.is_empty(x, y)):
            return None
        return self.board[x][y].nazwa

    def is_valid_target(self, x, y, frakcja, czy_sztab=False):
        if(not self.on_board(x, y)):
            return False
        if(self.is_empty(x, y)):
            return False
        if(self.get_type(x, y) == frakcja):
            return False
        if(czy_sztab and self.get_name(x, y) == "sztab"):
            return False
        return True

    def is_empty(self, x, y):
        return (self.board[x][y] == None)

    def on_board(self, x, y):
        if(not isinstance(x, int)):
            return False
        if(x < 0 or x >= self.width):
            return False
        if(not isinstance(y, int)):
            return False
        if(y < 0 or y >= self.length):
            return False
        return True  

    def get_type(self, x, y):
        if(not self.on_board(x, y)):
            return None
        if(self.board[x][y] is None):
            return None
        return self.board[x][y].frakcja

    def update_available_hexs(self, type):
        if(isinstance(type, bool)):
            for x in range(self.width):
                for y in range(self.length):
                    self.available_hexs[x][y] = type
            return
        
        for x in range(self.width):
            for y in range(self.length):
                if(self.get_type(x, y) == type):
                    self.available_hexs[x][y] = True
                else:
                    self.available_hexs[x][y] = False
        
        if(isinstance(type, dict)):
            self.available_hexs[type["x"]][type["y"]] = "rotate" 

    def bitwa(self):
        for inicjatywa in range(self.max_inicjatywa, -1, -1):
            for x in range(self.width):
                for y in range(self.length):
                    if(self.is_empty(x, y)):
                        continue
                    self.board[x][y].activate(self, inicjatywa)
            
            for x in range(self.width):
                for y in range(self.length):
                    if(self.is_empty(x, y)):
                        continue
                    if(not self.board[x][y].koniec_inicjatywy()):
                        self.board[x][y] = None
    
    # ----- Sieciarze -----
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

        for x in range(self.width):
            for y in range(self.length):
                akt = self.board[x][y]

                if akt is None or not akt.czy_sieciarz():
                    continue
                
                self.wszyscy_sieciarze.add((x, y))
                self.graf_sieciarzy[(x, y)]
                self.odwr_sieciarzy[(x, y)]

                kierunki = akt["siec"]

                for kier in kierunki:
                    kier = (kier + akt.rotacja + 6) % 6 # albo odwrotnie nwm
                    nx, ny = self.go(x, y, kier)

                    # print(f"Sieciarz ({x},{y}) frakcja {akt.frakcja} kierunek {kier} -> ({nx},{ny})")

                    if not self.is_valid_target(nx, ny, akt.frakcja):
                        continue

                    cel = self.board[nx][ny]

                    if cel is None or not cel.czy_sieciarz():
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

        return self.status_sieciarzy

        # print("--------------------------------------------\n")

    def go(self, x, y, direction):
        return (x + self.roza[direction]["x"], y + self.roza[direction]["y"])

    def print_board(self):
        for i in range(self.width):
            row = []
            for j in range(self.length):
                if(self.board[i][j] is None):
                    row.append(None)
                else:
                    # print(type(board.board[i][j]))
                    row.append((self.board[i][j].nazwa, self.board[i][j].rotacja))
                    # row.append(self.board[i][j].zeton_to_json())
            print(row)

    def wszystkie_jednostki(self):
        answer = []
        for x in range(self.width):
            for y in range(self.length):
                if(self.is_empty(x, y)):
                    continue
                answer.append([x, y, self.board[x][y].zeton_to_json()])
        return answer

    def import_board(self, data):
        for x in range(self.width):
            for y in range(self.length):
                pole = data[x][y]
                if(pole is None):
                    self.board[x][y] = None
                else:
                    self.postaw_zeton(x, y, pole)


    def board_to_json(self):
        json_board = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    json_board[i][j] = self.board[i][j].zeton_to_json()
        return json_board