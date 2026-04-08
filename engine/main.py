from copy import deepcopy
from plansza import Board
import wszystkie_frakcje
from akcje import Actions
from random import shuffle

class Game:
    def __init__(self, data):
        self.board = Board()
        self.faza = data["faza"]
        self.available_actions = {}
        self.game_over = 0
        self.bottoms = ["koniec tury", "kosz", "użyj", "cancel", "tak", "nie"]
        self.actions = Actions(self)


        if(self.faza == "newgame"):
            self.start_game(data["frakcje"]["player1"], data["frakcje"]["player2"])

        else:
            self.import_game_state(data)

            # status = True
            # while(status):
            status = self.actions.handler(self)
            if(status != None):
                self.user_actions.clear()
                self.actions.default_available_actions(self)
            
    def setup_pile(self, frakcja):
        for nazwa in wszystkie_frakcje.frakcje.get(frakcja, {}):
            for _ in range(wszystkie_frakcje.frakcje[frakcja][nazwa]["liczbajednostek"]):
                self.pile[frakcja].append(nazwa)
        shuffle(self.pile[frakcja])


    def start_game(self, frakcja1, frakcja2):
        self.current_frakcja = None
        self.user_actions = []
        self.next_turns = []
        self.next_turns.append({"frakcja" : frakcja1, "typ" : "wystaw_sztab"})
        self.next_turns.append({"frakcja" : frakcja2, "typ" : "wystaw_sztab"})
        self.pile = {
                    frakcja1 : [], 
                    frakcja2 : []
                    }
        self.setup_pile(frakcja1)
        self.setup_pile(frakcja2)

        self.hand = {frakcja1 : [], frakcja2 : []}
        # self.faza = "gra"
        self.actions.poczatek_tury(self)
        # print("FAZA:", self.faza)
        self.actions.default_available_actions(self)

    def import_game_state(self, data):
        # print("Importing game state...")
        self.faza = data["faza"]
        self.next_turns = data["next_turns"]
        self.current_frakcja = data["current_frakcja"]
        self.user_actions = data["user_actions"]
        self.board.import_board(data["board"])
        self.pile = data["pile"]
        self.hand = data["hand"]
        self.available_actions = data["available_actions"]
        for frakcja in self.hand.keys():
            self.actions.resize_hand(self.hand[frakcja])

        # self.actions.print_game_state(self)
        

    def export_game_state(self):
        print("Exporting game state...")
        self.actions.print_game_state(self)
        for frakcja in self.hand.keys():
            self.actions.fill_hand(self.hand[frakcja])
        data = {
                "faza" : self.faza,
                "next_turns" : self.next_turns,
                "current_frakcja" : self.current_frakcja,
                "user_actions" : self.user_actions,
                "board" : self.board.board_to_json(), 
                "pile" : self.pile,
                "hand" : self.hand,
                "available_actions" : self.available_actions
                }
        # print(data)
        return data
