from dataclasses import dataclass, field
from enum import Enum
from main.utils.variable import Bottom
from main.state.contex import ActionContext
from main.state.user_action import UserAction
from main.workflows.data import WorkflowData, WorkflowName
from typing import Callable, TypeVar, Generic

class StepType(Enum):
    INPUT = "input"
    AUTOMATIC = "automatic"

class StepName(Enum):
    INPUT = "input"
    INIT_WORKFLOW = "init_workflow"
    RESOLVE = "resolve"

@dataclass
class StepConfig():
    name : StepType | None = None


def no_bottoms(ctx : ActionContext) -> list[Bottom]:
    return []

def no_positions(ctx : ActionContext) -> list[tuple[int, int]]:
    return []

def no_tokens(ctx : ActionContext) -> dict[str, list[int]]:
    return {}

BottomsGetter = Callable[[ActionContext], list[Bottom]]
PositionsGetter = Callable[[ActionContext], list[tuple[int, int]]]
TokensGetter = Callable[[ActionContext], dict[str, list[int]]]

A = TypeVar("A", bound=UserAction)
T = TypeVar("T")

@dataclass
class InputStepConfig(StepConfig, Generic[A]):
    getter          : Callable[[A], T]
    setter          : Callable[[WorkflowData, T], None]
    consume_action  : bool = True
    get_bottoms     : BottomsGetter = no_bottoms
    get_positions   : PositionsGetter = no_positions
    get_tokens      : TokensGetter = no_tokens

@dataclass
class AutomaticStepConfig(StepConfig):
    pass

@dataclass
class ResolveStepConfig(AutomaticStepConfig):
    resolve_func : Callable[[ActionContext], None] | None = None
    wf_finished : bool = False

@dataclass
class InitStepConfig(AutomaticStepConfig):
    decision_func : Callable[[ActionContext], WorkflowName] | None = None
    as_child : bool = True
