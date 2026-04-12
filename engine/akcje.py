from copy import deepcopy

from collections import defaultdict
import wszystkie_frakcje
from variable import *
from zeton import Zeton
from sieciarze import Sieciarze

class Actions:
    def __init__(self, game):
        self.MAX_HAND_SIZE = 3
        self.bottoms = [Bottom.END_TURN, Bottom.DISCARD, Bottom.USE, Bottom.CANCEL, Bottom.YES, Bottom.NO]
        self.available_structure = {
            UI.HAND : False,
            UI.BOTTOM : {bottom : False for bottom in self.bottoms}
        }
        self.bottom_handlers = {
            Bottom.END_TURN : self.handle_end_turn,
            Bottom.DISCARD : self.handle_discard,
            Bottom.CANCEL : self.handle_cancel,
            Bottom.USE : self.handle_use
        }
        self.action_handlers = {
            Action.Type.BOARD : self.handle_board,
            Action.Type.HAND : self.handle_hand,
            Action.Type.ROTATE : self.handle_rotate,
            Action.Type.BOTTOM : self.handle_bottom,
        }
        self.instant_token_handlers = {
            Token.Type.Instant.BITWA : self.bitwa,
            Token.Type.Instant.MOVE : self.ruch,
        }

        self.validate_handlers = {
            Action.Type.BOARD : self.validate_board_action,
            Action.Type.HAND : self.validate_hand_action,
            Action.Type.BOTTOM : self.validate_bottom_action,
            Action.Type.ROTATE : self.validate_rotate_action
        }

        self.state_handlers = {
            State.SELECTED_HAND : self.hand_available_actions,
            State.NO_SELECTION : self.default_available_actions,
            State.MOVING : self.available_actions_ruch,
            State.ROTATE : self.rotate_available_actions,
            State.PLACING : self.placing_available_actions
        }

    #############################################################################
    #   Board functions       
    #############################################################################
    def wstawianie(self, game, action, nazwa):
        print("Wstawianie:", action, nazwa)
        board = game.board
        frakcja = game.current_frakcja
        hand = game.hand[frakcja]
        if((nazwa is None) or (self.get_zeton_type(nazwa, frakcja) != Token.Type.BOARD)):
            return False

        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        if(not board.on_board(x, y)):
            return False

        if(not board.is_empty(x, y)):
            return False
        
        self.odrzuc(hand, game.selected[Selected.SLOT])
        # zeton = Zeton.default_token
        # zeton[Token.NAME] = nazwa
        # zeton[Token.FRACTION] = frakcja
        game.board.postaw_zeton(x, y, Zeton.clear_token(nazwa, frakcja))
        game.state = State.ROTATE
        game.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : nazwa}
        return True
    
    def kwestia_sieciarzy(self, board):
        Sieciarze().kwestia_sieciarzy(board)

    #############################################################################
    #   Instant tokens functions 
    #############################################################################
    def available_actions_bitwa(self, game):
        # print("bitwa available actions")
        available = self.available_structure
        game.board.update_available_hexs([], [], None)
        if(self.koniec_tury(game, True)):
            available[UI.BOTTOM][Bottom.USE] = True

        available[UI.BOTTOM][Bottom.DISCARD] = True
        # print("available:", available)
        self.update_available_actions(game, available)

    def use_bitwa(self, game):
        if(game.state != State.SELECTED_HAND):
            return False
        if(not self.koniec_tury(game)):
            return False
        
        game.next_turns.insert(0, {Turn.FRACTION : Turn.BITWA, Turn.TYPE : None})
        self.poczatek_tury(game)
        return True
    
    def run_bitwa(self, game):
        game.board.bitwa()
        self.koniec_tury(game)
        self.poczatek_tury(game)
        return True

    def bitwa(self, game, mode):
        # print("bitwa")
        if(mode == Mode.RUN):
            return self.run_bitwa(game)
        if(mode == Mode.AVAILABLE_ACTIONS):
            self.available_actions_bitwa(game)
        if(mode == Mode.USE):
            self.use_bitwa(game)

    def available_actions_ruch(self, game):
        available = deepcopy(self.available_structure)
        if(game.state == State.SELECTED_HAND):
            game.board.update_available_hexs([game.current_frakcja], game.board.ALL_HEXES, game.board.can_move)
            available[UI.BOTTOM][Bottom.DISCARD] = True
            available[UI.BOTTOM][Bottom.CANCEL] = True
        
        if(game.state == State.MOVING):
            x = game.selected[Selected.X]
            y = game.selected[Selected.Y]
            adj = game.board.adjacent_hexes(x, y)
            game.board.update_available_hexs([None], adj, None)
            available[UI.BOTTOM][Bottom.CANCEL] = True

        self.update_available_actions(game, available)

    def use_ruch(self, game):
        action = game.action
        print("state:", game.state)
        if(game.state == State.SELECTED_HAND):
            x = action[Action.Key.X]
            y = action[Action.Key.Y]
            name = game.board.get_name(x, y)
            game.state = State.MOVING
            game.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : name}
            # self.available_actions_ruch(game)
            return True

        if(game.state == State.MOVING):
            x = game.selected[Selected.X]
            y = game.selected[Selected.Y]
            nx = action[Action.Key.X]
            ny = action[Action.Key.Y]
            game.board.przenies(x, y, nx, ny)
            game.state = State.ROTATE
            game.selected[Selected.X] = nx
            game.selected[Selected.Y] = ny
            
        return True
    
    def ruch(self, game, mode):
        if(mode == Mode.AVAILABLE_ACTIONS):
            self.available_actions_ruch(game)
        if(mode == Mode.USE):
            return self.use_ruch(game)
    
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

    def odrzuc(self, hand, slot):
        hand.pop(slot)

    def dociag(self, hand, pile):
        while(len(hand) < self.MAX_HAND_SIZE and len(pile) > 0):
                self.dobierz(hand, pile, pile[-1])

    def get_from_hand(self, hand, click):
        if(not isinstance(click, int)):
            return None

        if(len(hand) <= click):
            return None

        return hand[click]

    #############################################################################
    #   Turn functions       
    #############################################################################
    def poczatek_tury(self, game):
        if(game.current_frakcja != None):
            return False
        frakcja = game.next_turns[0][Turn.FRACTION]
        typ = game.next_turns[0][Turn.TYPE]
        game.current_frakcja = frakcja
        
        if(frakcja == Turn.BITWA):
            self.bitwa(game, Mode.RUN)
            return True

        if(typ == Turn.Type.HQ_PLACEMENT):
            game.faza = Phase.HQ_PLACEMENT
            self.dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

        else:
            game.faza = Phase.GAME
            self.dociag(game.hand[frakcja], game.pile[frakcja])

        if(len(game.pile[frakcja]) == 0):
            game.next_turns.append({Turn.FRACTION : Turn.BITWA, Turn.TYPE : Turn.Type.LAST})

        self.prepare_for_new_action(game)
        return True

    def koniec_tury(self, game, check=False):
        print("check:", check)
        print("next turns:", game.next_turns)
        next_turn = game.next_turns[0]
        frakcja = next_turn[Turn.FRACTION]
        typ = next_turn[Turn.TYPE]

        if((typ == Turn.Type.HQ_PLACEMENT) and (len(game.hand[frakcja]) > 0)):
            return False
        
        # if(frakcja == "bitwa"):
        #     return True
        
        if(frakcja != Turn.BITWA and len(game.hand[frakcja]) == self.MAX_HAND_SIZE):
            return False
        
        if(check):
            return True
        
        game.next_turns.pop(0)
        game.next_turns.append({Turn.FRACTION : frakcja, Turn.TYPE : Turn.Type.STANDARD})
        game.current_frakcja = None
        return True

    #############################################################################
    #   General functions       
    #############################################################################
    def get_zeton_type(self, nazwa, frakcja):
        return wszystkie_frakcje.frakcje.get(frakcja, {}).get(nazwa, {}).get(Token.TYPE, None)

    def invalid_move(self, message=""):
        print("INVALID MOVE")
        if(message):
            print(message)

    #############################################################################
    #   Validation functions       
    #############################################################################

    def validate_board_action(self, game, action):
        x = action.get(Action.Key.X, None)
        y = action.get(Action.Key.Y, None)
        if(not isinstance(x, int) or not isinstance(y, int)):
            return False
        if(not game.board.on_board(x, y)):
            return False
        return game.available_actions[UI.BOARD][x][y]

    def validate_hand_action(self, game, action):
        slot = action.get(Action.Key.SLOT, None)
        if(not isinstance(slot, int)):
            return False
        if(slot >= len(game.hand[game.current_frakcja])):
            return False
        return game.available_actions[UI.HAND][game.current_frakcja][slot]

    def validate_bottom_action(self, game, action):
        name = action.get(Action.Key.BOTTOM, None)
        if(name not in self.bottoms):
            return False
        return game.available_actions[UI.BOTTOM][name]

    def validate_rotate_action(self, game, action):
        rotation = action.get(Action.Key.ROTATION, None)
        if(not isinstance(rotation, int)):
            return False
        return True

    def validate_action(self, game, action):
        type = action[Action.Key.TYPE]
        function = self.validate_handlers.get(type, None)
        if(function is None):
            return False
        return function(game, action)

    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def default_available_actions(self, game):
        available = deepcopy(self.available_structure)
        if(self.koniec_tury(game, check=True)):
            available[UI.BOTTOM][Bottom.END_TURN] = True
        
        game.board.update_available_hexs([], [], None)
        available[UI.HAND] = True

        self.update_available_actions(game, available)

    def rotate_available_actions(self, game):
        x = game.selected[Selected.X]
        y = game.selected[Selected.Y]
        available = deepcopy(self.available_structure)
        game.board.update_available_hexs([game.current_frakcja], [(x, y)], None)
        self.update_available_actions(game, available)

    def placing_available_actions(self, game):
        available = deepcopy(self.available_structure)
        game.board.update_available_hexs([None], game.board.ALL_HEXES, None)

        available[UI.BOTTOM][Bottom.CANCEL] = True
        if(game.faza != Phase.HQ_PLACEMENT):
            available[UI.BOTTOM][Bottom.DISCARD] = True
        
        self.update_available_actions(game, available)

    def hand_available_actions(self, game):
        name = game.selected[Selected.NAME]
        function = self.instant_token_handlers.get(name, None)
        if(function is None):
            return False
        function(game, Mode.AVAILABLE_ACTIONS)

        return True

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
        game.available_actions[UI.HAND] = self.update_hand_available_actions(game.current_frakcja, game.hand, available_actions[UI.HAND])
        game.available_actions[UI.BOARD] = game.board.available_hexs
        game.available_actions[UI.BOTTOM] = available_actions[UI.BOTTOM]
        # print(game.available_actions["board"])

    def user_available_actions(self, game):
        function = self.state_handlers.get(game.state, None)
        if(function is None):
            return False
        function(game)
        return True


    #############################################################################
    #   Bottoms functions      
    #############################################################################
    def handle_end_turn(self, game):
        self.poczatek_tury(game)
        self.prepare_for_new_action(game)
        return True

    def handle_cancel(self, game):
        self.prepare_for_new_action(game)
        return True
    
    def handle_use(self, game):
        nazwa = game.selected[Selected.NAME]
        function = self.instant_token_handlers.get(nazwa, None)
        if function is None:
            return False
        
        return function(game, Mode.USE)

    def handle_discard(self, game):
        self.odrzuc(self.game.hand[game.current_frakcja], self.selected[Selected.SLOT])
        self.prepare_for_new_action(game)
        return True

    #############################################################################
    #   Handler functions      
    #############################################################################
    def prepare_for_new_action(self, game):
        if(game.state == State.ROTATE):
            self.kwestia_sieciarzy(game.board)
        game.state = State.NO_SELECTION
        game.selected = None

    def handle_board(self, game, action):
        # print("handle_board")
        name = game.selected[Selected.NAME]
        if game.state == State.PLACING:
            return self.wstawianie(game, action, name)
        
        elif(game.state == State.SELECTED_HAND):
            function = self.instant_token_handlers.get(name, None)
            if(function is None):
                return False
            return function(game, Mode.USE)
            
        elif(game.state == State.MOVING):
            return self.ruch(game, Mode.USE)

        else:
            return False
        
    def handle_hand(self, game, action):
        hand = game.hand[game.current_frakcja]
        nazwa = self.get_from_hand(hand, action[Action.Key.SLOT])
        type = self.get_zeton_type(nazwa, game.current_frakcja)

        if(type == Token.Type.BOARD):
            game.state = State.PLACING
        
        if(type == Token.Type.INSTANT):
            game.state = State.SELECTED_HAND
        game.selected = {Selected.SLOT : action[Action.Key.SLOT], Selected.NAME : nazwa}
        return True

    def handle_bottom(self, game, action):
        name = action[Action.Key.BOTTOM]
        function = self.bottom_handlers.get(name, None)
        return function(game)
        
    def handle_rotate(self, game, action):
        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        rotation = action[Action.Key.ROTATION]
        game.board.rotate(x, y, rotation)
        self.prepare_for_new_action(game)
        return True


    def handler(self, game):
        action = game.action
        if(action is None):
            return None
        
        print("USER ACTION:", action)
        if(not self.validate_action(game, action)):
            return False
        
        function = self.action_handlers.get(action[Action.Key.TYPE], None)
        return function(game, action)