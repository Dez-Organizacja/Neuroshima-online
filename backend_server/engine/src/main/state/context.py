from main.state.game_state import GameState
from main.rules.faction_manager import FactionManager
from main.state.player_state import PlayerState
from main.systems.undo import UndoSystem

class ActionContext():
    def __init__(
            self, 
            state : GameState, 
            faction_manager : FactionManager,
            undo_system : UndoSystem | None = None,
        ):
        self.state = state
        self.factions = faction_manager 
        self.undo_system = undo_system or UndoSystem()
        self.consumed_input : bool = False
        # self.decision_faction : str | None = None

    @property
    def phase(self):
        return self.state.phase

    #shortcuts
    @property
    def faction(self):
        return self.state.active_faction
    
    @faction.setter
    def faction(self, value):
        self.state.active_faction = value

    @property
    def board(self):
        return self.state.board

    @property
    def player(self) -> PlayerState:
        return self.state.players[self.faction]

    @property
    def workflow_data(self):
        return self.state.workflow_data
    
    @workflow_data.setter
    def workflow_data(self, value):
        self.state.workflow_data = value

    @property
    def workflow_instance(self):
        return self.state.workflow_stack[-1]

    @property
    def pending_attacks(self):
        return self.state.pending_attacks

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
