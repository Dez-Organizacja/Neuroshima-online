from dataclasses import dataclass, field
from main.workflows.data import WorkflowInstance
from typing import Callable
from main.state.contex import GameState
from main.input.data import UserAction

@dataclass
class TileDelta:
    pos : tuple[int, int]
    unit : dict

    def apply(self, state : GameState):
        if state.board.is_empty(self.pos):
            state.board.import_token(self.pos, self.unit)
        
        else:
            token = state.board.get_token(self.pos) 
            for k, v in self.unit.items():
                setattr(token, k, v)

@dataclass
class TilePlace:
    pos : tuple[int, int]
    name : str
    faction : str

    def apply(self, state : GameState):
        state.board.put_token(pos=self.pos, name=self.name, faction=self.faction)

@dataclass
class TileRemove:
    pos : tuple[int, int]

    def apply(self, state : GameState):
        state.board.remove_token(self.pos)

@dataclass
class StackPush:
    instance: WorkflowInstance
    def apply(self, state: GameState):
        # print(f"push {self.instance}")
        state.workflow_stack.append(self.instance)

@dataclass
class StackPop:
    def apply(self, state: GameState):
        # print("pop")
        state.workflow_stack.pop()

@dataclass
class StackSetIndex:
    index: int

    def apply(self, state: GameState):
        # print(f"set index to {self.index}")
        state.workflow_stack[-1].current_step_index = self.index

@dataclass
class HandAdd:
    card: str
    faction : str

    def apply(self, state: GameState):
        state.players[self.faction].hand.add(self.card)

@dataclass
class HandRemove:
    faction : str
    index: int

    def apply(self, state: GameState):
        state.players[self.faction].hand.remove(self.index)

StackChange = StackPush | StackPop | StackSetIndex
BoardDelta = TileDelta | TileRemove
HandDelta = HandAdd | HandRemove

@dataclass
class Delta:
    board_delta : list[BoardDelta] = field(default_factory=list)

    hand_delta : list[HandDelta] = field(default_factory=list)

    wf_data_delta : dict = field(default_factory=dict)
    stack_delta : list[StackChange] = field(default_factory=list)
    faction_delta : str | None = None
    turn_faction_delta : str | None = None

    def apply(self, state : GameState):
        if self.faction_delta is not None:
            state.active_faction = self.faction_delta
        
        if self.turn_faction_delta is not None:
            state.turn_faction = self.turn_faction_delta

        for tile in self.board_delta:
            tile.apply(state)

        # print("appling workflow stack changes")
        for stack_change in self.stack_delta:
            stack_change.apply(state)
        # print("workflow changes appiled")
        # print("-------------")
        
        for hand_change in self.hand_delta:
            hand_change.apply(state)

        for k, v in self.wf_data_delta.items():
            setattr(state.workflow_data, k, v)
        

@dataclass
class StepCase:
    action : UserAction
    delta : Delta = field(default_factory=Delta)

@dataclass
class Scenario:
    factions : list[str]
    steps : list[StepCase]
    setup : Delta = field(default_factory=Delta)