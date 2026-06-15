from dataclasses import dataclass, field
from main.workflows.data import WorkflowInstance
from typing import Callable
from main.state.context import GameState
from main.input.data import UserAction
from main.actions.available.data import AvailableStructure
from main.workflows.data import WorkflowInstance


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
class Delta:
    changes : list[Callable[[GameState], None]] = field(default_factory=list)

    def add(self, *funcs : Callable[[GameState], None]):
        self.changes.extend(funcs)

    def apply(self, state : GameState):
        for func in self.changes:
            func(state)
        

@dataclass
class StepCase:
    action : UserAction
    delta : Delta = field(default_factory=Delta)
    available_actions : AvailableStructure | None = None
    finish : bool = False

@dataclass
class Scenario:
    factions : list[str]
    steps : list[StepCase]
    setup : Delta = field(default_factory=Delta)
