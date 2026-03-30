from copy import deepcopy
from plansza import Board
import wszystkie_frakcje
import akcje

class Game:
    def __init__(self, data):
        self.board = Board()
        self.faza = data["faza"]
        self.game_over = 0
        self.available_actions = {}
        if(self.faza == "poczatek"):
            self.start_game(data["frakcje"]["player1"], data["frakcje"]["player2"])

        else:
            self.next_turns = data["next_turns"]
            self.current_frakcja = data["current_frakcja"]
            self.user_actions = data["user_actions"]
            self.board.import_board(data["board"])
            self.pile = data["pile"]
            self.hand = data["hand"]
            status = akcje.co_zrobic(self)
            if(status == True):
                self.user_actions.clear()

    def start_game(self, frakcja1, frakcja2):
        self.current_frakcja = None
        self.user_actions = []
        self.next_turns = []
        self.next_turns.append({"frakcja" : frakcja1, "typ" : "wystaw_sztab"})
        self.next_turns.append({"frakcja" : frakcja2, "typ" : "wystaw_sztab"})
        self.armie = [frakcja1, frakcja2]
        self.pile = {
                    frakcja1 : [nazwa for nazwa in wszystkie_frakcje.frakcje.get(frakcja1, {})], 
                    frakcja2 : [nazwa for nazwa in wszystkie_frakcje.frakcje.get(frakcja2, {})]
                    }
        self.hand = {frakcja1 : [], frakcja2 : []}
        self.faza = "gra"
        akcje.poczatek_tury(self)

    # def postaw_zeton(self, zeton):
    #     self.board.postaw_zeton(zeton["x"], zeton["y"], zeton)

    def export_game_state(self):
        data = {
                "faza" : self.faza,
                "next_turns" : self.next_turns,
                "current_frakcja" : self.current_frakcja,
                "user_actions" : self.user_actions,
                "board" : self.board.board_to_json(), 
                "pile" : self.pile,
                "hand" : self.hand,
                }
        # print(data)
        return data
