from copy import deepcopy

from collections import defaultdict
import wszystkie_frakcje
from variable import *
from zeton import Zeton
from sieciarze import Sieciarze
from instant_token import InstantToken
from battle import Battle

class Actions:
    def __init__(self, game):
        # self.MAX_HAND_SIZE = game.MAX_HAND_SIZE
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

        self.validate_handlers = {
            Action.Type.BOARD : self.validate_board_action,
            Action.Type.HAND : self.validate_hand_action,
            Action.Type.BOTTOM : self.validate_bottom_action,
            Action.Type.ROTATE : self.validate_rotate_action
        }

        self.state_handlers = {
            State.SELECTED_HAND : self.hand_available_actions,
            State.NO_SELECTION : self.default_available_actions,
            # State.MOVING : InstantToken(Token.Type.Instant.MOVE).available_actions,
            State.ROTATE : self.rotate_available_actions,
            State.PLACING : self.placing_available_actions,
            # State.SELECTED_PUSHer : InstantToken(Token.Type.Instant.PUSH).available_actions,
        }

    #############################################################################
    #   Board functions       
    #############################################################################
    def wstawianie(self, state, action, name):
        # print("Wstawianie:", action, name)
        fraction = state.current_fraction
        # hand = game.hand[frakcja]
        if((name is None) or (self.get_zeton_type(name, fraction) != Token.Type.BOARD)):
            return False

        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        
        state.current_player.hand.discard_token(name)
        # self.odrzuc(hand, game.selected[Selected.NAME])
        state.board.postaw_zeton(x, y, Zeton.clear_token(name, fraction))
        state.state = State.ROTATE
        state.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : name}
        state.active_action = {}
        return True
    
    def kwestia_sieciarzy(self, board):
        Sieciarze().kwestia_sieciarzy(board)

    #############################################################################
    #   Turn functions       
    #############################################################################
    def poczatek_tury(self, state):
        if(state.current_frakcja != None):
            return False
        fraction = state.next_turns[0][Turn.FRACTION]
        type = state.next_turns[0][Turn.TYPE]
        state.current_frakcja = fraction
        
        if(fraction == Turn.BITWA):
            Battle(state)
            return True

        player = state.current_player
        if(type == Turn.Type.HQ_PLACEMENT):
            state.phase = Phase.HQ_PLACEMENT
            # self.dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

        else:
            state.phase = Phase.GAME
        
        player.draw_tokens(type)

        if(player.pile.is_empty()):
            state.next_turns.append({Turn.FRACTION : Turn.BITWA, Turn.TYPE : Turn.Type.LAST})

        self.prepare_for_new_action(state)
        return True

    def koniec_tury(self, state, check=False):
        # print("check:", check)
        # print("next turns:", game.next_turns)
        next_turn = state.next_turns[0]
        frakcja = next_turn[Turn.FRACTION]
        typ = next_turn[Turn.TYPE]
        player = state.current_player

        if(player.hand.is_full()):
            return False
        
        if(check):
            return True
        
        state.next_turns.pop(0)
        state.next_turns.append({Turn.FRACTION : frakcja, Turn.TYPE : Turn.Type.STANDARD})
        state.current_fraction = None
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

    def validate_board_action(self, state, action):
        x = action.get(Action.Key.X, None)
        y = action.get(Action.Key.Y, None)
        if(not isinstance(x, int) or not isinstance(y, int)):
            return False
        if(not state.board.on_board(x, y)):
            return False
        return True
        # return state.available_actions[UI.BOARD][x][y]

    def validate_hand_action(self, state, action):
        slot = action.get(Action.Key.SLOT, None)
        if(not isinstance(slot, int)):
            return False
        
        if(state.current_player.hand.get_token(slot) is None):
            return False
        return True
        # return game.available_actions[UI.HAND][game.current_frakcja][slot]

    def validate_bottom_action(self, game, action):
        name = action.get(Action.Key.BOTTOM, None)
        if(name not in game.bottoms):
            return False
        return Turn
        # return game.available_actions[UI.BOTTOM][name]

    def validate_rotate_action(self, state, action):
        rotation = action.get(Action.Key.ROTATION, None)
        if(not isinstance(rotation, int)):
            return False
        return True

    def validate_action(self, game, action):
        if (action is None):
            return True
        type = action.get(Action.Key.TYPE, None)
        function = self.validate_handlers.get(type, None)
        if(function is None):
            return False
        return function(game, action)

    
   
    #############################################################################
    #   Bottoms functions      
    #############################################################################
    def handle_end_turn(self, game):
        self.poczatek_tury(game)
        self.koniec_tury(game)
        self.prepare_for_new_action(game)
        return True

    def handle_cancel(self, game):
        self.prepare_for_new_action(game)
        return True
    
    def handle_use(self, game):
        InstantToken(game.active_action).resolve(game, Mode.USE)
        return True

    def handle_discard(self, game):
        self.odrzuc(self.game.hand[game.current_frakcja], self.selected[Selected.SLOT])
        self.prepare_for_new_action(game)
        return True

    #############################################################################
    #   Handler functions      
    #############################################################################
    def prepare_for_new_action(self, game):
        self.kwestia_sieciarzy(game.board)
        game.state = State.NO_SELECTION
        game.selected = None
        game.active_action = None

    def handle_board(self, game, action):
        print("handle_board")
        # print(f"Selected token: {name}")
        if game.state == State.PLACING:
            name = game.selected[Selected.NAME]
            return self.wstawianie(game, action, name)
        
        InstantToken(game.active_action).resolve(game, Mode.USE)
        return True
        
    def handle_hand(self, game, action):
        hand = game.hand[game.current_frakcja]
        nazwa = self.get_from_hand(hand, action[Action.Key.SLOT])
        type = self.get_zeton_type(nazwa, game.current_frakcja)
        print("handle_hand")
        print(f"Selected token: {nazwa}, type: {type}")

        if(type == Token.Type.BOARD):
            game.state = State.PLACING
            game.active_action = None
        
        if(type == Token.Type.INSTANT):
            game.state = State.SELECTED_HAND
            game.active_action = nazwa
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
            return True
        
        print("USER ACTION:", action)
        print("Validating game state...")
        if(not self.validate_action(game, action)):
            return False
        
        print(f"action: {action} is valid")
        function = self.action_handlers.get(action[Action.Key.TYPE], None)
        return function(game, action)