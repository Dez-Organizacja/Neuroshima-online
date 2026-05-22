from dataclasses import dataclass
from abc import ABC
from main.actions.available.config import AvActionsConfig
from main.state.contex import ActionContext
from main.state.user_action import UserAction
from main.steps.data import StepResult, StepName
from main.workflows.data import WorkflowData, WorkflowName, WorkflowConfig
from main.events.data import ActionResult
from typing import Callable, TypeVar, Generic

@dataclass
class StepConfig(ABC):
    name : StepName


@dataclass
class WaitingStepConfig(StepConfig):
    name              : StepName = StepName.WAITING
    av_actions_config : AvActionsConfig
    consume_action    : bool = True
     
@dataclass
class AutomaticStepConfig(StepConfig):
    pass

def no_result_function(ctx : ActionContext) -> StepResult:
    return StepResult()

@dataclass
class ResolveStepConfig(AutomaticStepConfig):
    name         : StepName = StepName.RESOLVE
    resolve_func : Callable[[ActionContext], StepResult] = no_result_function
    wf_finished  : bool = False

C = TypeVar("C", bound=WorkflowConfig)
@dataclass
class InitStepConfig(AutomaticStepConfig):
    name          : StepName = StepName.INIT
    decision_func : Callable[[ActionContext], WorkflowName] | None = None
    wf_name       : WorkflowName | None = None
    as_child      : bool = True

A = TypeVar("A", bound=UserAction)
T = TypeVar("T")
@dataclass 
class SetStepConfig(AutomaticStepConfig, Generic[A]):
    name            : StepName = StepName.SET
    getter          : Callable[[A], T]
    setter          : Callable[[WorkflowData, T], None]

@dataclass
class EndTurnCheckConfig(AutomaticStepConfig):
    repeat_from_index : int = 0
    check_func : Callable[[ActionContext], bool]
    resolve_func : Callable[[ActionContext], ActionResult] = no_result_function