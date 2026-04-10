from copy import deepcopy

import wszystkie_frakcje
from variable import *

class Actions:
    def __init__(self, game):
        self.MAX_HAND_SIZE = 3
        self.bottoms = [Bottom.END_TURN, Bottom.DISCARD, Bottom.USE, Bottom.CANCEL,Bottom.YES, Bottom.NO]
        self.available_structure = {
            "hand" : False,
            "bottoms" : {bottom : False for bottom in self.bottoms}
        }
        self.bottom_handlers = {
            Bottom.END_TURN : self.handle_end_turn,
            Bottom.CANCEL : self.handle_cancel,
            Bottom.USE : self.handle_use
        }
        self.action_handlers = {
            Action_Type.BOARD : self.handle_board,
            Action_Type.HAND : self.handle_hand,
            Action_Type.ROTATE : self.handle_rotate,
            Action_Type.BOTTOM : self.handle_bottom,
        }
        self.instant_token_handlers = {
            Instant_Token.BITWA : self.use_bitwa,
        }

    #############################################################################
    #   Board functions       
    #############################################################################
    def wstawianie(self, game, action, nazwa):
        # print("Wstawianie:", action, nazwa, frakcja)
        board = game.board
        frakcja = game.current_frakcja
        hand = game.hand[frakcja]
        if((nazwa is None) or (self.get_zeton_type(nazwa, frakcja) != "plansza")):
            return False

        x = action["x"]
        y = action["y"]
        if(not board.on_board(x, y)):
            return False

        if(not board.is_empty(x, y)):
            return False
        
        self.odrzuc(hand, nazwa)
        zeton = {"nazwa" : nazwa, "frakcja" : frakcja, "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(x, y, zeton)
        board.update_available_hexs([], [(x, y)], None)
        
        self.update_available_actions(game, deepcopy(self.available_structure))
        game.state = State.ROTATE
        game.selected = {"x" : x, "y" : y}
        return True

    #############################################################################
    #   Instant tokens functions 
    #############################################################################
    def available_actions_bitwa(self, game):
        available = self.available_structure
        game.board.update_available_hexs([], [], None)
        if(self.koniec_tury(game, True)):
            available["bottoms"]["uzyj"] = True

        available["bottoms"]["discard"] = True
        self.update_available_actions(game, available)

    def use_bitwa(self, game, use=True):
        if(not use):
            self.available_actions_bitwa(game)
            return None
        
        if(game.state != State.SELECTED_HAND):
            return False
        if(not self.koniec_tury(game)):
            return False
        
        game.next_turns.insert(0, {"frakcja" : "bitwa", "typ" : None})
        self.poczatek_tury(game)
        return True
    
    def run_bitwa(self, game):
        game.board.bitwa()
        self.koniec_tury(game)
        self.poczatek_tury(game)
        return True


    def bitwa(self, game, mode):
        if(mode == Variable.RUN):
            return self.run_bitwa(game)
        if(mode == Variable.AVAILABLE_ACTIONS):
            self.available_actions_bitwa()
        if(mode == Variable.USE):
            self.use_bitwa()
    
    #############################################################################
    #   Hand functions       
    #############################################################################
    def resize_hand(self, hand):
        while(len(hand) > 0 and hand[-1] is None):
            hand.pop(-1)

    def fill_hand(self, hand):
        while(len(hand) < self.MAX_HAND_SIZE):
            hand.append(None)

    def dobierz(self, hand, pile, nazwa):
        hand.append(nazwa)
        pile.remove(nazwa)

    def odrzuc(self, hand, zeton):
        hand.remove(zeton)

    def dociag(self, hand, pile):
        while(len(hand) < self.MAX_HAND_SIZE and len(pile) > 0):
                self.dobierz(hand, pile, pile[-1])

    def get_from_hand(self, hand, click):
        if(not isinstance(click, int)):
            return None

        if(len(hand) <= click):
            return None

        return hand[click]

    def hand_available_actions(self, game):
        frakcja = game.current_frakcja
        name = game.hand[frakcja][game.selected["slot"]]
        type = self.get_zeton_type(name, frakcja)
        if(type == Token_Type.ON_BOARD):
            available = deepcopy(self.available_structure)
            game.board.update_available_hexs([None], game.board.ALL_HEXES, None)

            available["bottoms"][Bottom.CANCEL] = True
            if(game.faza != "sztaby"):
                available["bottoms"][Bottom.DISCARD] = True

        if(type == Token_Type.INSTANT):
            function = self.instant_token_handlers.get(name, None)
            available = function(game, Variable.AVAILABLE_ACTIONS)

        self.update_available_actions(game, available)

    #############################################################################
    #   Turn functions       
    #############################################################################
    def poczatek_tury(self, game):
        if(game.current_frakcja != None):
            return False
        frakcja = game.next_turns[0]["frakcja"]
        typ = game.next_turns[0]["typ"]
        game.current_frakcja = frakcja
        
        if(frakcja == Variable.BITWA):
            self.bitwa(game)
            return True

        if(typ == Turn_Type.HQ_PLACEMENT):
            game.faza = "sztaby"
            self.dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

        else:
            game.faza = "tura"
            self.dociag(game.hand[frakcja], game.pile[frakcja])

        if(len(game.pile[frakcja]) == 0):
            game.next_turns.append({"frakcja" : "bitwa", "typ" : "ostatnia"})

        return True

    def koniec_tury(self, game, check=False):
        next_turn = game.next_turns[0]
        frakcja = next_turn["frakcja"]
        typ = next_turn["typ"]

        if((typ == Turn_Type.HQ_PLACEMENT) and (len(game.hand[frakcja]) > 0)):
            return False
        
        # if(frakcja == "bitwa"):
        #     return True
        
        if(frakcja != "bitwa" and len(game.hand[frakcja]) == 3):
            return False
        
        if(check):
            return True
        
        game.next_turns.pop(0)
        game.next_turns.append({"frakcja" : frakcja, "typ" : "tura"})
        game.current_frakcja = None
        return True

    #############################################################################
    #   General functions       
    #############################################################################
    def get_zeton_type(self, nazwa, frakcja):
        return wszystkie_frakcje.frakcje.get(frakcja, {}).get(nazwa, {}).get("typ", None)

    def invalid_move(self, user_actions):
        print("INVALID MOVE")
        user_actions.clear()
    
    def get_first(self, actions):
        if(actions is None or len(actions) == 0):
            return None
        
        return actions.pop(0)

    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def default_available_actions(self, game):
        available = deepcopy(self.available_structure)
        if(self.koniec_tury(game, check=True)):
            available["bottoms"][Bottom.END_TURN] = True
        
        game.board.update_available_hexs([], [], None)
        available["hand"] = True

        self.update_available_actions(game, available)

    def update_hand_available_actions(self, current_frakcja, hand, available_hand):
        actions = {key : [False for i in range(self.MAX_HAND_SIZE)] for key in hand.keys()}
        if(not available_hand):
            return actions
        
        for i in range(self.MAX_HAND_SIZE):
            if(self.get_from_hand(hand[current_frakcja], i) is not None):
                actions[current_frakcja][i] = True

        return actions

    def update_available_actions(self, game, available_actions):
        # print("AVAILABLE ACTIONS:", available_actions)
        game.available_actions = {}
        game.available_actions["hand"] = self.update_hand_available_actions(game.current_frakcja, game.hand, available_actions["hand"])
        game.available_actions["board"] = game.board.available_hexs
        game.available_actions["bottoms"] = available_actions["bottoms"]
        # print(game.available_actions["board"])

    #############################################################################
    #   Bottoms functions      
    #############################################################################
    def handle_end_turn(self, game):
        if(game.state != State.NO_SELECTION):
            return False
        
        if(not self.koniec_tury(game)):
            return False
        
        self.poczatek_tury(game)
        self.prepare_for_new_action(game)
        return True

    def handle_cancel(self, game):
        self.prepare_for_new_action(game)
        return True
    
    def handle_use(self, game):
        if game.state != State.SELECTED_HAND:
            return False
        frakcja = game.current_frakcja
        nazwa = self.get_from_hand(game.hand[frakcja], game.selected["slot"])
        function = self.instant_token_handlers.get(nazwa, None)
        if function is None:
            return False
        
        function(game, Variable.USE)

    #############################################################################
    #   Handler functions      
    #############################################################################
    def prepare_for_new_action(self, game):
        game.state = State.NO_SELECTION
        game.selected = None
        self.default_available_actions(game)

    def handle_board(self, game, action):
        if game.state == State.SELECTED_HAND:
            slot = game.selected["slot"]
            hand = game.hand[game.current_frakcja]
            name = self.get_from_hand(hand, slot)
            return self.wstawianie(game, action, name)

        else:
            return False
        
    def handle_hand(self, game, action):
        if game.state != State.NO_SELECTION:
            return False
        
        hand = game.hand[game.current_frakcja]
        nazwa = self.get_from_hand(hand, action["slot"])
        if(nazwa is None):
            # self.invalid_move(game.user_actions)
            return False

        game.state = State.SELECTED_HAND
        game.selected = {"slot" : action["slot"]}
        self.hand_available_actions(game)
        return True

    def handle_bottom(self, game, action):
        name = action["bottom"]
        if(not game.available_actions["bottoms"][name]):
            return False

        function = self.bottom_handlers.get(name, None)
        if(function is not None):
            return function(game)
        else:
            return False

    def handle_rotate(self, game, action):
        x = action["x"]
        y = action["y"]
        rotation = action["rotation"]
        game.board.rotate(x, y, rotation)
        self.prepare_for_new_action(game)
        return True


    def handler(self, game):
        action = game.action
        print("USER ACTION:", action)
        # if(action is None):
        #     return None
        
        function = self.action_handlers.get(action["type"], None)
        if(function is not None):
            return function(game, action)
            
        else:
            return False