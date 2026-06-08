from main.state.game_state import GameState
from main.rules.game import GameRules
from main.state.player_state import PlayerState

class ActionContext():
    def __init__(
            self, 
            state : GameState, 
            rules : GameRules | None = None, 
        ):
        self.state = state
        self.rules = rules or GameRules()
        self.consumed_input : bool = False

    #shortcuts
    @property
    def selected(self):
        return self.state.selected
    
    @property
    def faction(self):
        return self.state.current_faction
    
    @faction.setter
    def faction(self, value):
        self.state.current_faction = value

    @property
    def board(self):
        return self.state.board

    @property
    def player(self) -> PlayerState:
        return self.state.players[self.faction]

    @property
    def ui_state(self):
        return self.state.interaction_state
    
    @property
    def workflow_data(self):
        return self.state.workflow_data
    
    @workflow_data.setter
    def workflow_data(self, value):
        self.state.workflow_data = value

    @property
    def workflow_instance(self):
        return self.state.workflow_stack[-1]
    
    def print_wf_stack(self):
        print("stack")
        for instance in self.state.workflow_stack:
            print("name: ", instance.name)
        print("---------")

    def str_flow_queue(self):
        queue = []
        for flow in self.state.flow_queue:
            queue.append(type(flow).__name__)
        return queue
