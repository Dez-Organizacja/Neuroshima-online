from dataclasses import dataclass, field
from main.workflows.data import WorkflowInstance
from typing import Callable
from main.state.contex import GameState
from main.input.data import UserAction

@dataclass
class TileDelta:
    pos : tuple[int, int]
    unit : dict

@dataclass
class StackChange:
    pop : bool = False
    add : WorkflowInstance | None = None

@dataclass
class Delta:
    expected_step_index : int | None = None

    board_delta : list[TileDelta] = field(default_factory=list)
    board_remove : list[tuple[int, int]] = field(default_factory=list)

    hand_add : list[str] = field(default_factory=list)
    hand_remove : list[int] = field(default_factory=list)

    wf_data_delta : dict = field(default_factory=dict)
    stack_delta : list[StackChange] = field(default_factory=list)
    faction_delta : str | None


@dataclass
class StepCase:
    action : UserAction
    delta : Delta = field(default_factory=Delta)

@dataclass
class Scenario:
    @staticmethod
    def no_setup_func(ctx : GameState):
        pass
    factions : list[str]
    steps : list[StepCase]
    setup : Delta = field(default_factory=Delta)