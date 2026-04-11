from copy import deepcopy
import wszystkie_frakcje

class Zeton:
        def __init__(self,  x, y, data):
            self.frakcja = data["frakcja"]
            self.nazwa = data["nazwa"]
            self.rotacja = data["rotacja"]
            self.rany = data["rany"]
            self.x = x
            self.y = y
            self.wlasciwosci_pierwotne = wszystkie_frakcje.frakcje.get(self.frakcja, {}).get(self.nazwa, {})
            self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)
            self.zasiecowany = False
            self.attack_functions = {
                "melee" : self.melee,
                "shoot" : self.shoot,
                "gauss" : self.gauss
            }

        def __getitem__(self, key):
            # pozwala robis self["xd"] zamiast self.wlasciwosci["xd"]
            return self.wlasciwosci.get(key)
        
        def zeton_to_json(self):
            json = {
                "frakcja": self.frakcja,
                "nazwa": self.nazwa,
                "rotacja": self.rotacja,
                "rany": self.rany,
                "zasiecowany": self.zasiecowany
            }
            return json
        
        def zasieciuj(self):
            self.zasiecowany = True
        
        def odsieciuj(self):
            self.zasiecowany = False

        def czy_sieciarz(self):
            return ("siec" in self.wlasciwosci)

        def czy_w_planszy(self, x, y):
            return (0 <= x < 5 and 0 <= y < 9)

        def rotate(self, rotacja):
            if (self.zasiecowany):
                return 0
            
            self.rotacja = rotacja
            return 1

        def dostan_rane(self, obrazenia, kierunek, czy_blokowalny=False):
            # kierunek -> skad przychodzi atak
            # print("dostalem rane", self.frakcja, self.nazwa, obrazenia, kierunek, czy_blokowalny)
            
            kierunek2 = (kierunek - self.rotacja + 6) % 6
            pancerz = self.wlasciwosci.get("pancerz", {})

            if (kierunek2 in pancerz) and (czy_blokowalny):
                obrazenia -= 1

            self.rany += obrazenia

        def koniec_inicjatywy(self):
            return(self["hp"] > self.rany)
            # if self["hp"] <= self.rany:
            #     # wywolaj_medyka()
            #     self.board[self.x][self.y] = None

        def melee(self, board, x, y, direction, power):
            czy_sztab = (self.nazwa == "sztab")
            # print()
            # frakcja = board.get_type(x, y)
            nx, ny = board.go(x, y, direction)

            # print(f"melee: ({x},{y}) -> ({nx},{ny}), kierunek {direction}, power {power}")
            if(not board.on_board(nx, ny)):
                return
            
            if(not board.is_valid_target(nx, ny, self.frakcja, czy_sztab)):
                return

            print(f"melee: ({x},{y}) -> ({nx},{ny}), jestem {self.frakcja}, {self.nazwa}, kierunek {direction}, power {power}")
            board.board[nx][ny].dostan_rane(power, direction)

        def shoot(self, board, x, y, direction, power):
            # frakcja = board.get_type(x, y)

            nx, ny = x, y
            while(not board.is_valid_target(nx, ny, self.frakcja) and board.on_board(nx, ny)):
                nx, ny = board.go(nx, ny, direction)

            if(not board.is_valid_target(nx, ny, self.frakcja)):
                return
            
            board.board[nx][ny].dostan_rane(power, direction, True)

        def gauss(self, board, x, y, direction, power):
            # self.frakcja = board.get_type(x, y)
            nx, ny = x, y
            while(board.on_board(nx, ny)):
                if(board.is_valid_target(nx, ny, self.frakcja)):
                    board.board[nx][ny].dostan_rane(power, direction, True)
                nx, ny = board.go(nx, ny, direction)

        def is_boost(self, frakcja):
            if self.frakcja != frakcja:
                return False
            
            return "wzmocnienia" in self.wlasciwosci

        def boost(self, board):
            self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)

            if (self.zasiecowany):
                return
            
            for i in range(6):
                nx, ny = board.go(self.x, self.y, i)

                if (self.czy_w_planszy(nx, ny) == 0):             
                    continue

                cel = board.board[nx][ny]

                if cel is None or not cel.is_boost(self.frakcja):
                    continue

                wzmocnienia = cel.wlasciwosci["wzmocnienia"]                   
                
                for wzmocnienie in wzmocnienia.keys():
                    if "wzmocniony_atak" in wzmocnienie:
                        if "ataki" in self.wlasciwosci and "melee" in self.wlasciwosci["ataki"]:
                                for i in range(len(self.wlasciwosci["ataki"]["melee"])):
                                    self.wlasciwosci["ataki"]["melee"][i][1] += 1
                    elif "wzmocniony_strzal" in wzmocnienie:
                        if "ataki" in self.wlasciwosci and "shoot" in self.wlasciwosci["ataki"]:
                                for i in range(len(self.wlasciwosci["ataki"]["shoot"])):
                                    self.wlasciwosci["ataki"]["shoot"][i][1] += 1
                    elif "wyzsza_inicjatywa" in wzmocnienie:
                        if "inicjatywa" in self.wlasciwosci:
                            for i in range(len(self.wlasciwosci["inicjatywa"])):
                                self.wlasciwosci["inicjatywa"][i] += 1

            # print("Zboostowalem", self.frakcja, self.nazwa, self.wlasciwosci)
                    
        def activate(self, board, inicjatywa):
            if (self.zasiecowany):
                # print("Jestem zasieciowany, nie moge atakowac, smuteczek", self.frakcja, self.nazwa)
                return
            
            if(inicjatywa not in self.wlasciwosci.get("inicjatywa", [])):
                return
            
            print("aktywacja", self.nazwa, self.frakcja)
            ataki = self.wlasciwosci["ataki"]

            for type in ataki.keys():
                attack_function = self.attack_functions.get(type)
                for (direction, power) in ataki[type]:
                    direct = (direction + self.rotacja) % 6

                    print(f"Atak {type} z ({self.x},{self.y}) w kierunku {direct} o sile {power}, na {board.go(self.x, self.y, direct)}")
                    attack_function(board, self.x, self.y, direct, power)


            # if "inicjatywa" in self.wlasciwosci and nr_inicjatywy in self["inicjatywa"]:
            #     if ("atak" in self.wlasciwosci):
            #         # print(self.frakcja, self.nazwa, nr_inicjatywy)

            #         for atak, sila in self["atak"]:
            #             atak_obr = (atak + self.rotacja) % 6
            #             nowyx = self.x + self.roza[atak_obr][0]
            #             nowyy = self.y + self.roza[atak_obr][1]
                        
            #             if self.czy_w_planszy(nowyx, nowyy) and self.board[nowyx][nowyy] is not None:
            #                 # print("nowyx, nowyy: ", nowyx, nowyy)
            #                 if self.board[nowyx][nowyy].frakcja != self.frakcja:
            #                     self.board[nowyx][nowyy].dostan_rane(sila, (atak_obr + 3) % 6, "atak")

            #     if ("strzal" in self.wlasciwosci):
            #         # print(self.frakcja, self.nazwa, nr_inicjatywy)

            #         for strzal, sila in self["strzal"]:
            #             strzal_obr = (strzal + self.rotacja) % 6
            #             nowyx = self.x + self.roza[strzal_obr][0]
            #             nowyy = self.y + self.roza[strzal_obr][1]
                        
            #             while self.czy_w_planszy(nowyx, nowyy):
            #                 # print("nowyx, nowyy: ", nowyx, nowyy)

            #                 if self.board[nowyx][nowyy] is not None:
            #                     if self.board[nowyx][nowyy].frakcja != self.frakcja:
            #                         self.board[nowyx][nowyy].dostan_rane(sila, (strzal_obr + 3) % 6, "strzal")
            #                         break
            #                 nowyx += self.roza[strzal_obr][0]
            #                 nowyy += self.roza[strzal_obr][1]