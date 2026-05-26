from main.systems.sieciarze import Sieciarze
from main.utils.variable import *

class AkcjeNaPlanszy:
    def __init__(self, board):
        self.board = board

        self.attack_functions = {
            Attack.MELEE : self.melee,
            Attack.SHOOT : self.shoot,
            Attack.GAUSS : self.gauss
        }

    # --------- boosty ---------

    def czy_dobra_frakcja(self, boost_target, frakcja1, frakcja2):
        if (boost_target == "own"):
            return frakcja1 == frakcja2
        else:
            return frakcja1 != frakcja2
        
    def stealing_boosts(self):
        for x in range(self.board.width):
            for y in range(self.board.length):
                akt = self.board.board[x][y]

                if (akt is None or akt.czy_zasieciowany() or akt.czy_modul() == False):
                    continue

                boosts = akt.get_boosts()

                if Boost.STEAL_BOOST in boosts.keys():
                    for direction in boosts[Boost.STEAL_BOOST]:
                        nx, ny = self.board.go((x, y), direction)

                        if (not self.board.on_board((nx, ny))):
                            continue

                        cel = self.board.board[nx][ny]

                        if (cel is None or not self.czy_dobra_frakcja(akt.wlasciwosci.get(Token.Stats.BOOST_TARGET), akt.frakcja, cel.frakcja)):
                            continue
                        
                        # print(f"Steal Boost: ({x},{y}) -> ({nx},{ny}), kierunek {direction}, boost {boost_type}")
                        
                        cel.steal_boost()

    def boost_all(self):
        for x in range(self.board.width):
            for y in range(self.board.length):
                akt = self.board.board[x][y]

                if (akt is None or akt.czy_zasieciowany() or akt.czy_modul() == False):
                    continue

                boosts = akt.get_boosts()

                for boost_type in boosts.keys():
                    for direction in boosts[boost_type]:
                        nx, ny = self.board.go((x, y), direction)

                        if (not self.board.on_board((nx, ny))):
                            continue

                        cel = self.board.board[nx][ny]

                        if (cel is None or not self.czy_dobra_frakcja(akt.wlasciwosci.get(Token.Stats.BOOST_TARGET), akt.frakcja, cel.frakcja)):
                            continue
                        
                        # print(f"Boost: ({x},{y}) -> ({nx},{ny}), kierunek {direction}, boost {boost_type}")
                        
                        cel.boost_me(boost_type)

    # --------- reset ---------

    def reset_all(self):
        for x in range(self.board.width):
            for y in range(self.board.length):
                if (self.board.is_empty((x, y))):
                    continue
                self.board.board[x][y].reset_stats()

    # --------- sieciarze ---------

    def kwestia_sieciarzy(self):
        self.sieciarze = Sieciarze(self.board)

    # --------- aktywacja ---------

    def melee(self, x, y, direction, power, frakcja):
        czy_sztab = (self.board.board[x][y].nazwa == "sztab")
        nx, ny = self.board.go((x, y), direction)

        # print(f"melee: ({x},{y}) -> ({nx},{ny}), jestem {self.board.board[x][y].frakcja}, {self.board.board[x][y].nazwa}, kierunek {direction}, power {power}")
  
        if(not self.board.czy_w_planszy((nx, ny)) or not self.board.is_valid_target((nx, ny), frakcja, czy_sztab=czy_sztab)):
            return

        # print(f"melee: ({x},{y}) -> ({nx},{ny}), jestem {self.board.board[x][y].frakcja}, {self.board.board[x][y].nazwa}, kierunek {direction}, power {power}")
        self.board.board[nx][ny].attacked(power, direction)

    def shoot(self, x, y, direction, power, frakcja):
        nx, ny = self.board.go((x, y), direction)

        while(not self.board.is_valid_target((nx, ny), frakcja) and self.board.czy_w_planszy((nx, ny))):
            nx, ny = self.board.go((nx, ny), direction)

        if(not self.board.is_valid_target((nx, ny), frakcja)):
            return
        
        self.board.board[nx][ny].attacked(power, direction, True)

    def gauss(self, x, y, direction, power, frakcja):
        nx, ny = self.board.go((x, y), direction)

        while(self.board.czy_w_planszy((nx, ny))):
            if(self.board.is_valid_target((nx, ny), frakcja)):
                self.board.board[nx][ny].attacked(power, direction, True)
            nx, ny = self.board.go((nx, ny), direction)

    def aktywacja(self, inicjatywa):
        # print("--- faza aktywacji ---")

        for x in range(self.board.width):
            for y in range(self.board.length):
                if(self.board.is_empty((x, y))):
                    continue
                if (self.board.board[x][y].czy_zasieciowany()):
                    continue

                attacks = self.board.board[x][y].daj_ataki(inicjatywa)
                
                # print(f"Aktywacja: ({x},{y}), {self.board.board[x][y].nazwa}, ataki {attacks}")

                for type in attacks.keys():
                    attack_function = self.attack_functions.get(type)

                    for (direction, power) in attacks[type]:
                        # print(f"atak -> Jestem {self.board.board[x][y].nazwa}, atakuję {type} o sile {power} w {self.board.go(x, y, direction)}")
                        attack_function(x, y, direction, power, self.board.board[x][y].frakcja)
                # print("--------------")
