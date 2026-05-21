from copy import deepcopy
import main.frakcje.wszystkie_frakcje as allfractions
from main.utils.variable import *
from copy import deepcopy
from main.tokens.abstract_token import Token
from main.tokens.data import TokenKey, TokenStats, TokenType

class BoardToken(Token):
    DEFAULT = {
        TokenKey.NAME : "default",
        TokenKey.FRACTION : "neutral",
        TokenKey.ROTATION : 0,
        TokenKey.DAMAGE : 0,
        # TokenKey.X : -1,
        # TokenKey.Y : -1
        # Token.WIRED : False
    }
    TYPE = "board"

    def __init__(self, rules, name, fraction, data):
        merged = {**self.DEFAULT, **data}
        # print(data)
        # print("token.name:", Token.NAME)
        # self.frakcja = data[Token.FRACTION]
        # self.name = data[Token.NAME]
        super().__init__(rules, name, fraction, TokenType.BOARD)
        self.rotacja = merged[TokenKey.ROTATION]
        self.rany = merged[TokenKey.DAMAGE]
        # self.x = merged[TokenKey.X]
        # self.y = merged[TokenKey.Y]
        raw_wlasciwosci = allfractions.frakcje.get(
            self.fraction, {}
        ).get(self.name, {})
        self.wlasciwosci_pierwotne = raw_wlasciwosci
        
        self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)
        
        self.zasiecowany = False
        self.boost_to_attack = {
            Boost.MELEE: Attack.MELEE,
            Boost.SHOOT: Attack.SHOOT,
        }

    def __getitem__(self, key):
        # pozwala robis self["xd"] zamiast self.wlasciwosci["xd"]
        if isinstance(key, str):
            for stat in TokenStats:
                if stat.value == key:
                    key = stat
                    break
        return self.wlasciwosci.get(key)

    @property
    def nazwa(self):
        return self.name

    @property
    def frakcja(self):
        return self.fraction

    def export(self):
        return self.name

    def zeton_to_json(self):
        json = {
            Token.FRACTION: self.fraction,
            Token.NAME: self.name,
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
        return (TokenStats.WIRE in self.wlasciwosci)
    
    # --------- moduly ---------

    def czy_modul(self):
        return (TokenStats.BOOSTS in self.wlasciwosci)

    def get_boosts(self):
        return self.wlasciwosci.get(TokenStats.BOOSTS, {})
    
    def steal_boost(self):
        self.wlasciwosci[TokenStats.BOOST_TARGET] = "enemy"

    def boost_me(self, boost_type):
        if boost_type in self.boost_to_attack:
            attack_key = self.boost_to_attack[boost_type]

            attacks = self.wlasciwosci.get(TokenStats.ATTACKS)

            if attacks and attack_key in attacks:
                attack_list = attacks[attack_key]

                for i, (direction, power) in enumerate(attack_list):
                    attack_list[i] = (direction, power + 1)

                # print(f"Jestem {self.name}, mam boost {boost_type}, atak {attack_key}: {attack_list}")
            return

        if boost_type == Boost.INITIATIVE:
            initiative = self.wlasciwosci.get(TokenStats.INITIATIVE)

            if initiative:
                for i in range(len(initiative)):
                    initiative[i] += 1

    # -----------------------------------------

    def reset_stats(self):
        self.wlasciwosci = deepcopy(self.wlasciwosci_pierwotne)

    def czy_w_planszy(self, x, y):
        return (0 <= x < 5 and 0 <= y < 9)

    def rotate(self, rotacja):
        self.rotacja = rotacja
        
    def dostan_rane(self, obrazenia):
        self.rany += obrazenia

    def attacked(self, obrazenia, kierunek, czy_blokowalny=False):
        # kierunek -> skad przychodzi atak
        # print("dostalem rane", self.frakcja, self.name, obrazenia, kierunek, czy_blokowalny)
        print(f"{self.name} atakowany, obrazenia {obrazenia}, kierunek {kierunek}, czy_blokowalny {czy_blokowalny}")
        kierunek2 = (kierunek - self.rotacja + 6) % 6
        pancerz = self.wlasciwosci.get(TokenStats.ARMOR, {})

        if (kierunek2 in pancerz) and (czy_blokowalny):
            obrazenia -= 1

        self.dostan_rane(obrazenia)

    def is_alive(self):
        return(self[TokenStats.HP] > self.rany)
        # if self["hp"] <= self.rany:
        #     # wywolaj_medyka()
        #     self.board[self.x][self.y] = None

    def get_stat(self, stat_key):
        return self.wlasciwosci.get(stat_key, None)

    def can_activate(self, initiative):
        initiatives = self.get_stat(TokenStats.INITIATIVE)
        if initiatives:
            return initiative in initiative
        return False

    def daj_ataki(self, inicjatywa):
        if not self.can_activate(inicjatywa):
            return {}

        attacks = self.wlasciwosci.get(TokenStats.ATTACKS, {})
        
        ataki = {}
        for attack_type, attack_list in attacks.items():
            ataki[attack_type] = [[(direction + self.rotacja) % 6, power] for direction, power in attack_list]

        return ataki