import wszystkie_frakcje

class Zeton:
        def __init__(self,  x, y, frakcja, nazwa, rotacja, rany):
            self.wlasciwosci = wszystkie_frakcje.frakcje.get(frakcja, {}).get(nazwa, {})
            self.frakcja = frakcja
            self.nazwa = nazwa
            self.x = x
            self.y = y
            self.rotacja = rotacja
            self.rany = rany

        def __getitem__(self, key):
            # pozwala robis self["xd"] zamiast self.wlasciwosci["xd"]
            return self.wlasciwosci.get(key)
        
        def zeton_to_json(self):
            json = {
                "frakcja": self.frakcja,
                "nazwa": self.nazwa,
                "rotacja": self.rotacja,
                "rany": self.rany
            }
            return json

        def czy_w_planszy(self, x, y):
            return (0 <= x < 5 and 0 <= y < 9)

        def rotate(self, rotacja):
            self.rotacja = rotacja

        def dostan_rane(self, obrazenia, kierunek, jaki_atak):
            # kierunek -> skad przychodzi atak
            kierunek2 = (kierunek - self.rotacja + 6) % 6

            if "pancerz" in self.wlasciwosci and kierunek2 in self["pancerz"] and jaki_atak == "strzal":
                obrazenia -= 1

            self.rany += obrazenia

        def koniec_inicjatywy(self):
            if self["hp"] <= self.rany:
                # wywolaj_medyka()
                self.board[self.x][self.y] = None

        
        def aktywuj(self, nr_inicjatywy):
            if "inicjatywa" in self.wlasciwosci and nr_inicjatywy in self["inicjatywa"]:
                if ("atak" in self.wlasciwosci):
                    # print(self.frakcja, self.nazwa, nr_inicjatywy)

                    for atak, sila in self["atak"]:
                        atak_obr = (atak + self.rotacja) % 6
                        nowyx = self.x + self.roza[atak_obr][0]
                        nowyy = self.y + self.roza[atak_obr][1]
                        
                        if self.czy_w_planszy(nowyx, nowyy) and self.board[nowyx][nowyy] is not None:
                            # print("nowyx, nowyy: ", nowyx, nowyy)
                            if self.board[nowyx][nowyy].frakcja != self.frakcja:
                                self.board[nowyx][nowyy].dostan_rane(sila, (atak_obr + 3) % 6, "atak")

                if ("strzal" in self.wlasciwosci):
                    # print(self.frakcja, self.nazwa, nr_inicjatywy)

                    for strzal, sila in self["strzal"]:
                        strzal_obr = (strzal + self.rotacja) % 6
                        nowyx = self.x + self.roza[strzal_obr][0]
                        nowyy = self.y + self.roza[strzal_obr][1]
                        
                        while self.czy_w_planszy(nowyx, nowyy):
                            # print("nowyx, nowyy: ", nowyx, nowyy)

                            if self.board[nowyx][nowyy] is not None:
                                if self.board[nowyx][nowyy].frakcja != self.frakcja:
                                    self.board[nowyx][nowyy].dostan_rane(sila, (strzal_obr + 3) % 6, "strzal")
                                    break
                            nowyx += self.roza[strzal_obr][0]
                            nowyy += self.roza[strzal_obr][1]