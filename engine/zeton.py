from copy import deepcopy
import wszystkie_frakcje
from variable import *
from copy import deepcopy

class Zeton:
    DEFAULT = {
        TokenKey.NAME : "default",
        TokenKey.FRACTION : "neutral",
        TokenKey.ROTATION : 0,
        TokenKey.DAMAGE : 0,
        TokenKey.X : -1,
        TokenKey.Y : -1
        # Token.WIRED : False
    }

    @classmethod
    def clear_token(cls, name, fraction):
        token = deepcopy(cls.default_token)
        token[TokenKey.NAME] = name
        token[TokenKey.FRACTION] = fraction
        return token

    def __init__(self, name, fraction, data):
        merged = {**self.DEFAULT, **data}
        # print(data)
        # print("token.name:", Token.NAME)
        # self.frakcja = data[Token.FRACTION]
        # self.nazwa = data[Token.NAME]
        super().__init__(name, fraction)
        self.rotacja = merged[TokenKey.ROTATION]
        self.rany = merged[TokenKey.DAMAGE]
        self.x = merged[TokenKey.X]
        self.y = merged[TokenKey.Y]
        self.wlasciwosci_pierwotne = wszystkie_frakcje.frakcje.get(
            self.frakcja, {}
        ).get(self.nazwa, {})
        
        self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)
        
        self.zasiecowany = False
        self.boost_to_attack = {
            Boost.MELEE: Attack.MELEE,
            Boost.SHOOT: Attack.SHOOT,
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

    # --------- sieciarze ---------

    def zasieciuj(self):
        self.zasiecowany = True
    
    def odsieciuj(self):
        self.zasiecowany = False

    def czy_zasieciowany(self):
        return self.zasiecowany

    def czy_sieciarz(self):
        return (Token.Stats.WIRE in self.wlasciwosci)
    
    # --------- moduly ---------

    def czy_modul(self):
        return (Token.Stats.BOOSTS in self.wlasciwosci)

    def get_boosts(self):
        return self.wlasciwosci.get(Token.Stats.BOOSTS, {})

    def boost_me(self, boost_type):
        if boost_type in self.boost_to_attack:
            attack_key = self.boost_to_attack[boost_type]

            attacks = self.wlasciwosci.get(Token.Stats.ATTACKS)

            if attacks and attack_key in attacks:
                attack_list = attacks[attack_key]

                for i, (direction, power) in enumerate(attack_list):
                    attack_list[i] = (direction, power + 1)

                # print(f"Jestem {self.nazwa}, mam boost {boost_type}, atak {attack_key}: {attack_list}")
            return

        if boost_type == Boost.INITIATIVE:
            initiative = self.wlasciwosci.get(Token.Stats.INITIATIVE)

            if initiative:
                for i in range(len(initiative)):
                    initiative[i] += 1

    # -----------------------------------------

    def reset_stats(self):
        self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)

    def czy_w_planszy(self, x, y):
        return (0 <= x < 5 and 0 <= y < 9)

    def rotate(self, rotacja):
        if (self.zasiecowany):
            return 0
        
        self.rotacja = rotacja
        return 1

    def dostan_rane(self, obrazenia):
        self.rany += obrazenia
        # kierunek -> skad przychodzi atak
        # print("dostalem rane", self.frakcja, self.nazwa, obrazenia, kierunek, czy_blokowalny)

    def attacked(self, obrazenia, kierunek, czy_blokowalny=False):
        print(f"{self.nazwa} atakowany, obrazenia {obrazenia}, kierunek {kierunek}, czy_blokowalny {czy_blokowalny}")
        kierunek2 = (kierunek - self.rotacja + 6) % 6
        pancerz = self.wlasciwosci.get(Token.Stats.ARMOR, {})

        if (kierunek2 in pancerz) and (czy_blokowalny):
            obrazenia -= 1

        self.dostan_rane(obrazenia)

    def is_alive(self):
        return(self[Token.Stats.HP] > self.rany)
        # if self["hp"] <= self.rany:
        #     # wywolaj_medyka()
        #     self.board[self.x][self.y] = None

    def daj_ataki(self, inicjatywa):
        if (inicjatywa not in self.wlasciwosci.get(Token.Stats.INITIATIVE, [])):
            return {}

        attacks = self.wlasciwosci.get(Token.Stats.ATTACKS, {})
        
        ataki = {}
        for attack_type, attack_list in attacks.items():
            ataki[attack_type] = [[(direction + self.rotacja) % 6, power] for direction, power in attack_list]

        return ataki