from dataclasses import dataclass, field
from main.utils.variable import Bottom
from main.state.contex import ActionContext
from main.state.user_action import UserAction
from main.workflows.data import WorkflowData
from typing import Callable, TypeVar, Generic
A = TypeVar("A", bound=UserAction)
T = TypeVar("T")


def no_available_tokens(ctx : ActionContext) -> dict[str, list[int]]:
    return {}

def no_positions(ctx : ActionContext) -> list[tuple[int, int]]:
    return []

@dataclass
class StepConfig(Generic[A]):
    getter          : Callable[[A], T]
    setter          : Callable[[WorkflowData, T], None]
    allowed_bottoms : list[Bottom] = field(default_factory=list)
    get_positions   : Callable[
        [ActionContext], 
        list[tuple[int, int]]
    ] = no_positions

    get_available_tokens : Callable[
        [ActionContext], 
        dict[str, list[int]]
    ] = no_available_tokens