from main.state.game_state import GameState
from main.rules.game import GameRules
from main.state.player_state import PlayerState

class ActionContext():
    def __init__(
            self, 
            state : GameState, 
            rules : GameRules, 
        ):
        self.state = state
        self.rules = rules
        self.consumed_input : bool = False

    #shortcuts
    @property
    def selected(self):
        return self.state.selected
    
    @property
    def fraction(self):
        return self.state.current_fraction
    
    @property
    def board(self):
        return self.state.board

    @property
    def player(self) -> PlayerState:
        return self.state.current_player
    
    @property
    def active_token(self):
        token = self.player.hand.get_active_token()
        if token:
            return token
        else:
            return self.board.get_tile(self.selected.unit_position)

    @property
    def ui_state(self):
        return self.state.interaction_state
    
    @property
    def workflow_data(self):
        return self.state.workflow_data
    
    @property
    def workflow_instance(self):
        return self.state.workflow_stack[-1]