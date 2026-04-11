from copy import deepcopy
import wszystkie_frakcje
from variable import *
from copy import deepcopy

class Zeton:
        default_token = {
            Token.NAME : None,
            Token.FRACTION : None,
            Token.ROTATION : 0,
            Token.DAMAGE : 0,
            # Token.WIRED : False
        }

        @classmethod
        def clear_token(cls, name, fraction):
            token = deepcopy(cls.default_token)
            token[Token.NAME] = name
            token[Token.FRACTION] = fraction
            return token
    
        def __init__(self,  x, y, data):
            # print(data)
            # print("token.name:", Token.NAME)
            self.frakcja = data[Token.FRACTION]
            self.nazwa = data[Token.NAME]
            self.rotacja = data[Token.ROTATION]
            self.rany = data[Token.DAMAGE]
            self.x = x
            self.y = y
            self.wlasciwosci_pierwotne = wszystkie_frakcje.frakcje.get(self.frakcja, {}).get(self.nazwa, {})
            self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)
            self.zasiecowany = False
            self.attack_functions = {
                Attack.MELEE : self.melee,
                Attack.SHOOT : self.shoot,
                Attack.GAUSS : self.gauss
            }

        def __getitem__(self, key):
            # pozwala robis self["xd"] zamiast self.wlasciwosci["xd"]
            return self.wlasciwosci.get(key)
        
        def zeton_to_json(self):
            json = {
                Token.FRACTION: self.frakcja,
                Token.NAME: self.nazwa,
                Token.ROTATION: self.rotacja,
                Token.DAMAGE: self.rany,
                Token.WIRED: self.zasiecowany
            }
            return json
        
        def zasieciuj(self):
            self.zasiecowany = True
        
        def odsieciuj(self):
            self.zasiecowany = False

        def czy_zasieciowany(self):
            return self.zasiecowany

        def czy_sieciarz(self):
            return (Token.Stats.WIRE in self.wlasciwosci)

        # def czy_w_planszy(self, x, y):
        #     return (0 <= x < 5 and 0 <= y < 9)

        def rotate(self, rotacja):
            if (self.zasiecowany):
                return 0
            
            self.rotacja = rotacja
            return 1

        def dostan_rane(self, obrazenia, kierunek, czy_blokowalny=False):
            # kierunek -> skad przychodzi atak
            # print("dostalem rane", self.frakcja, self.nazwa, obrazenia, kierunek, czy_blokowalny)
            
            kierunek2 = (kierunek - self.rotacja + 6) % 6
            pancerz = self.wlasciwosci.get(Token.Stats.ARMOR, {})

            if (kierunek2 in pancerz) and (czy_blokowalny):
                obrazenia -= 1

            self.rany += obrazenia

        def koniec_inicjatywy(self):
            return(self[Token.Stats.HP] > self.rany)
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

            # print(f"melee: ({x},{y}) -> ({nx},{ny}), jestem {self.frakcja}, {self.nazwa}, kierunek {direction}, power {power}")
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
            
            if(inicjatywa not in self.wlasciwosci.get(Token.Stats.INITIATIVE, [])):
                return
            
            # print("aktywacja", self.nazwa, self.frakcja)
            ataki = self.wlasciwosci[Token.Stats.ATTACKS]

            for type in ataki.keys():
                attack_function = self.attack_functions.get(type)
                for (direction, power) in ataki[type]:
                    direct = (direction + self.rotacja) % 6
                    attack_function(board, self.x, self.y, direct, power)