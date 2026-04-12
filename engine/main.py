from copy import deepcopy
from plansza import Board
import wszystkie_frakcje
from akcje import Actions
from akcje import State
from random import shuffle
from variable import *

class Game:
    def __init__(self, data):
        self.board = Board()
        self.actions = Actions(self)
        self.faza = data["faza"]
        self.available_actions = {}
        self.game_over = False


        if(self.faza == "newgame"):
            self.start_game(data["frakcje"]["player1"], data["frakcje"]["player2"])

        else:
            self.import_game_state(data)

            # status = True
            # while(status):
            if(not self.actions.handler(self)):
                self.actions.invalid_move()

            if(not self.actions.user_available_actions(self)):
                print("INVALID STATE")

    def setup_pile(self, frakcja):
        for nazwa in wszystkie_frakcje.frakcje.get(frakcja, {}):
            for _ in range(wszystkie_frakcje.frakcje[frakcja][nazwa][Token.UNIT_COUNT]):
                self.pile[frakcja].append(nazwa)
        shuffle(self.pile[frakcja])


    def start_game(self, frakcja1, frakcja2):
        self.state = State.NO_SELECTION
        self.selected = None
        self.current_frakcja = None
        # self.user_actions = []
        self.next_turns = []
        self.next_turns.append({Turn.FRACTION : frakcja1, Turn.TYPE : Turn.Type.HQ_PLACEMENT})
        self.next_turns.append({Turn.FRACTION : frakcja2, Turn.TYPE : Turn.Type.HQ_PLACEMENT})
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
        self.action = data["action"]
        # self.user_actions = data["user_actions"]
        self.state = data["state"]
        self.selected = data["selected"]
        self.board.import_board(data["board"])
        self.actions.kwestia_sieciarzy(self.board)
        self.pile = data["pile"]
        self.hand = data["hand"]
        self.available_actions = data["available_actions"]
        for frakcja in self.hand.keys():
            self.actions.resize_hand(self.hand[frakcja])

        # self.actions.print_game_state(self)
        

    def export_game_state(self):
        print("Exporting game state...")
        self.print_game_state()
        for frakcja in self.hand.keys():
            self.actions.fill_hand(self.hand[frakcja])
        data = {
                "faza" : self.faza,
                "state" : self.state,
                "selected" : self.selected,
                "next_turns" : self.next_turns,
                "current_frakcja" : self.current_frakcja,
                # "user_actions" : self.user_actions,
                "board" : self.board.board_to_json(), 
                "pile" : self.pile,
                "hand" : self.hand,
                "available_actions" : self.available_actions
                }
        # print(data)
        return data
    
    def print_game_state(self):
        print("\n---------------------------\n")
        print("Faza:", self.faza)
        print("State:", self.state)
        print("Selected:", self.selected)
        print("Current frakcja:", self.current_frakcja)
        # print("Next_turns:", self.next_turns)
        print("Board:")
        self.board.print_board()
        for frakcja in self.hand.keys():
            print(frakcja)
            # print("Pile:", self.pile[frakcja])
            print("Hand:", self.hand[frakcja])
        print("Available actions:")
        self.print_available_actions(self.available_actions)
        print("\n---------------------------\n")

    def print_available_actions(self, available_actions):
        # print("Available actions:")
        print("Hand:", available_actions[UI.HAND])
        print("Board:")
        for x in range(self.board.width):
            row = []
            for y in range(self.board.length):
                if(not self.board.on_board(x, y)):
                    continue
                row.append(available_actions[UI.BOARD][x][y])
            print(row)
        print("Bottoms:", available_actions[UI.BOTTOM])

