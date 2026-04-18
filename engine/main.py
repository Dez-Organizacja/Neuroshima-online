from copy import deepcopy
from plansza import Board
import wszystkie_frakcje
from akcje import Actions
from akcje import State
from variable import *
from player_state import PlayerState
from game_state import GameState
from random import shuffle

class Game:
    bottoms = [Bottom.END_TURN, Bottom.DISCARD, Bottom.USE, Bottom.CANCEL, Bottom.YES, Bottom.NO]
    available_structure = {
        UI.HAND : False,
        UI.BOTTOM : {bottom : False for bottom in bottoms}
    }

    def __init__(self, data):
        fractions = data['fractions']
        if(isinstance(fractions, dict)):
            data['fractions'] = [fractions["player1"], fractions["player2"]]
        print("data:", data)
        self.state = GameState.from_dict(data)
        self.actions = Actions(self)
        # self.board = Board()
        # self.faza = data["faza"]
        # self.frakcje = data["frakcje"]
        # self.available_actions = {}
        # self.players = {}
        # self.game_over = False

        if(self.state.phase == Phase.START_GAME):
            self.start_game()

        else:
            self.import_game_state(data)

            # status = True
            # while(status):
            
            if(not self.actions.handler(self)):
                self.actions.invalid_move()
                return
            
            if(not self.actions.user_available_actions(self)):
                print("INVALID STATE")


    def start_game(self):
        shuffle(self.state.fractions)
        self.state.current_fraction = self.state.fractions[0]
        for fraction in self.state.fractions:
            player = PlayerState(fraction)
            player.new_game()
            self.state.players[fraction] = player
            self.state.next_turns.append({Turn.FRACTION : fraction, Turn.TYPE : Turn.Type.HQ_PLACEMENT})
        self.state.phase = Phase.GAME
        # self.actions.poczatek_tury(self)
        # self.actions.default_available_actions(self)



        # self.state = State.NO_SELECTION
        # self.selected = None
        # self.active_action = None
        # self.current_frakcja = None
        # self.frakcje = [frakcja1, frakcja2]
        # # self.enemy = {self.frakcje[0] : self.frakcje[1], self.frakcje[1] : self.frakcje[0]}
        # # self.user_actions = []
        # self.next_turns = []
        # self.next_turns.append({Turn.FRACTION : frakcja1, Turn.TYPE : Turn.Type.HQ_PLACEMENT})
        # self.next_turns.append({Turn.FRACTION : frakcja2, Turn.TYPE : Turn.Type.HQ_PLACEMENT})
        # # self.hand = {frakcja1 : [], frakcja2 : []}
        # self.faza = "gra"
        # self.players = {fraction : PlayerState(fraction).new_game() for fraction in self.frakcje}
        # self.hand = Hand(self.frakcje)
        # print("FAZA:", self.faza)

    def import_game_state(self, data):
        print("Importing game state...")
        self.faza = data["faza"]
        self.frakcje = data["frakcje"]
        self.enemy = {self.frakcje[0] : self.frakcje[1], self.frakcje[1] : self.frakcje[0]}
        # print("Enemy mapping:", self.enemy)
        self.next_turns = data["next_turns"]
        self.current_frakcja = data["current_frakcja"]
        self.action = data["action"]
        # self.user_actions = data["user_actions"]
        self.state = data["state"]
        self.selected = data["selected"]
        self.active_action = data["active_action"]
        self.board.import_board(data["board"])
        # data_player_states = data["player_states"]

        for fraction, fraction_data in data["players"].items():
            self.players[fraction] = PlayerState(fraction).from_dict(fraction_data)

        # self.pile = data["pile"]
        # self.hand = Hand(self.frakcje).from_dict(data["hand"])
        # self.hand = data["hand"]
        self.available_actions = data["available_actions"]
        # for frakcja in self.hand.keys():
        #     self.actions.resize_hand(self.hand[frakcja])

        self.actions.kwestia_sieciarzy(self.board)
        # self.actions.print_game_state(self)
        

    def export_game_state(self):
        print("Exporting game state...")
        self.print_game_state()
        # for frakcja in self.hand.keys():
        #     self.actions.fill_hand(self.hand[frakcja])
        data = {
                "faza" : self.faza,
                "frakcje" : self.frakcje,
                "state" : self.state,
                "selected" : self.selected,
                "active_action" : self.active_action,
                "next_turns" : self.next_turns,
                "current_frakcja" : self.current_frakcja,
                # "user_actions" : self.user_actions,
                "board" : self.board.board_to_json(), 
                "players" : {
                    fraction : player_state.to_dict()
                    for fraction, player_state in self.player_states.items()
                },
                # "pile" : self.pile,
                # "hand" : self.hand.to_dict(),
                "available_actions" : self.available_actions
                }
        # print(data)
        return data
    
    def print_game_state(self):
        print("\n---------------------------\n")
        print("Faza:", self.faza)
        print("State:", self.state)
        print("Selected:", self.selected)
        print("Active action:", self.active_action)
        print("Current frakcja:", self.current_frakcja)
        # print("Next_turns:", self.next_turns)
        print("Board:")
        self.board.print_board()
        print("Players:")
        for fraction, state in self.players.items():
            print("Frakcja:", fraction)
            state.print_state()
            print("##########")
        # print("Hand:")
        # self.hand.print_hand()
        # for frakcja in self.hand.keys():
        #     print(frakcja)
        #     # print("Pile:", self.pile[frakcja])
        #     print("Hand:", self.hand[frakcja])
        # print("Available actions:")
        # self.print_available_actions(self.available_actions)
        # print("\n---------------------------\n")

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

