from variable import Selected, Phase

class Bottom:
    END_TURN = "end_turn"
    DISCARD = "discard"
    USE = "use"
    CANCEL = "cancel"
    YES = "yes"
    NO = "no"

class BoardFilter():
    def __init__(self, types=None, positions=None, predicate=None):
        self.types = types
        self.positions = positions
        self.predicate = predicate

class AvailableActions():
    BOTTOM_KEY = "bottom"
    HAND_KEY = "hand"
    BOARD_KEY = "board"
    all_bottoms = [Bottom.END_TURN, Bottom.DISCARD, Bottom.USE, Bottom.CANCEL, Bottom.YES, Bottom.NO]
    def __init__(self, state):
        self.hand = {
            fraction : [False for _ in range(player.hand.size())]
            for fraction, player in state.players.items()
        }
        self.board = {
            hex : False
            for hex in state.board.ALL_HEXES
        }
        self.bottoms = {
            bottom : False
            for bottom in self.all_bottoms
        }
        self.all_hexes_type = state.fractions + [None]
    
    def update_hand_availability(self, state, value):
        for i in range(state.current_player.hand.size()):
            self.hand[self.current_fraction][i] = value
        
    def update_board_availability(self, board, filter : BoardFilter):
        allowed_types = filter.types or self.all_types
        allowed_positions = filter.positions or board.ALL_HEXES
        predicate = filter.predicate
        for hex in board.ALL_HEXES:
            x, y = hex
            type = board.get_type(x, y)
            if(type not in allowed_types):
                self.board[x][y] = False
                continue
            
            if(hex not in allowed_positions):
                self.board[x][y] = False
                continue

            if(predicate is None):
                self.board[x][y] = True
                continue
            
            else:
                self.board[x][y] = board.predicate(x, y)
    
    def default_available_actions(self, state, actions):
        if(actions.koniec_tury(state, check=True)):
            self.enable(Bottom.END_TURN)
        
        # self.update_board_availability(state.board, self.all_hexes_type, state.board.ALL_HEXES, None)
        self.update_hand_availability(state, True)

    def rotate_available_actions(self, state):
        x = state.selected[Selected.X]
        y = state.selected[Selected.Y]
        # available = deepcopy(game.available_structure)
        filter = BoardFilter(
            type = [state.current_frakcja]
        )
        self.update_board_availability(state.board, filter)

    def enable(self, bottom):
        if bottom in self.all_bottomsbottoms:
            self.bottoms[bottom] = True

    def placing_available_actions(self, state):
        # available = deepcopy(game.available_structure)
        filter = BoardFilter(
            types=[None],
        )
        self.update_board_availability(state.board, filter)
        # state.board.update_available_hexs([None], game.board.ALL_HEXES, None)

        # available[UI.BOTTOM][Bottom.CANCEL] = True
        # self.bottom[Bottom.CANCEL] = True
        self.enable(Bottom.CANCEL)
        if(state.phase != Phase.HQ_PLACEMENT):
            self.enable(Bottom.DISCARD)
            # self.bottom[Bottom.DISCARD] = True
            # available[UI.BOTTOM][Bottom.DISCARD] = True
        
        # self.update_available_actions(game, available)

    def hand_available_actions(self, game):
        name = game.selected[Selected.NAME]
        InstantToken(game.active_action).resolve(game, Mode.AVAILABLE_ACTIONS)
        return True

    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def instant_taken_available_actions(self, game):
        name = game.active_action
        InstantToken(name).resolve(game, Mode.AVAILABLE_ACTIONS)

    def user_available_actions(self, game):
        print("Updating available actions...")
        print("Current state:", game.state)
        if(game.active_action is not None):
            print("active action:", game.active_action)
            self.instant_taken_available_actions(game)
            return True

        function = self.state_handlers.get(game.state, None)
        if(function is None):
            return False
        function(game)
        return True

