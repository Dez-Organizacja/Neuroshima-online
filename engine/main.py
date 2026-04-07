from copy import deepcopy
from plansza import Board
import wszystkie_frakcje
from akcje import Actions

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

            status = self.actions.handler(self)
            if(status != None):
                self.user_actions.clear()
                self.actions.default_available_actions(self)
            
           

    def start_game(self, frakcja1, frakcja2):
        self.current_frakcja = None
        self.user_actions = []
        self.next_turns = []
        self.next_turns.append({"frakcja" : frakcja1, "typ" : "wystaw_sztab"})
        self.next_turns.append({"frakcja" : frakcja2, "typ" : "wystaw_sztab"})
        self.pile = {
                    frakcja1 : [nazwa for nazwa in wszystkie_frakcje.frakcje.get(frakcja1, {})], 
                    frakcja2 : [nazwa for nazwa in wszystkie_frakcje.frakcje.get(frakcja2, {})]
                    }
        self.hand = {frakcja1 : [], frakcja2 : []}
        # self.faza = "gra"
        self.actions.poczatek_tury(self)
        # print("FAZA:", self.faza)
        self.actions.default_available_actions(self)

    # def poczatek_tury(self):
    #     if(self.current_frakcja != None):
    #         return False
    #     frakcja = self.next_turns[0]["frakcja"]
    #     typ = self.next_turns[0]["typ"]
        
    #     # if(frakcja == "bitwa"):
    #     #     bitwa()
    #     #     return

    #     self.current_frakcja = frakcja
    #     if(typ == "wystaw_sztab"):
    #         self.faza = "sztaby"
    #         self.dobierz(self.hand[frakcja], self.pile[frakcja], "sztab")

    #     else:
    #         self.faza = "tura"
    #         self.dociag(self.hand[frakcja], self.pile[frakcja])

    #     if(len(self.pile[frakcja]) == 0):
    #         self.next_turns.append({"frakcja" : "bitwa", "typ" : "ostatnia"})

    #     print("Faza:", self.faza)
    #     return True

    # def koniec_tury(self, check=False):

    #     next_turn = self.next_turns[0]
    #     frakcja = next_turn["frakcja"]
    #     typ = next_turn["typ"]

    #     if((typ == "wystaw_sztab") and (len(self.hand[frakcja]) > 0)):
    #         return False
        
    #     # if(frakcja == "bitwa"):
    #     #     return True
        
    #     if(len(self.hand[frakcja]) == 3):
    #         return False
        
    #     if(check):
    #         return True
        
    #     self.next_turns.pop(0)
    #     self.next_turns.append({"frakcja" : frakcja, "typ" : "tura"})
    #     self.current_frakcja = None
    #     return True

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
        # print("Exporting game state...")
        # self.actions.print_game_state(self)
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
