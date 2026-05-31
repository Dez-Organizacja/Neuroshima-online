from dataclasses import dataclass, field
from abc import ABC
from main.actions.available.config import AvailableActionProvider
from main.state.contex import ActionContext
from main.input.data import UserAction
from main.steps.data import StepResult, StepName
from main.workflows.data import WorkflowData, WorkflowConfig, WorkflowName
from typing import Callable, TypeVar, Generic
from main.input.action_handlers import ActionHandler
from main.events.data import ExecutionResult

@dataclass
class StepConfig(ABC):
    name : StepName = field(init=False)


@dataclass
class WaitingStepConfig(StepConfig):
    av_actions_provider : AvailableActionProvider = field(default_factory=AvailableActionProvider)
    action_handler     : ActionHandler = field(default_factory=ActionHandler)
    consume_action     : bool = True
    name               : StepName = field(default=StepName.WAITING, init=False)
    
@dataclass
class AutomaticStepConfig(StepConfig):
    pass


def no_result_function(ctx : ActionContext) -> ExecutionResult:
    return ExecutionResult()

@dataclass
class ResolveStepConfig(AutomaticStepConfig):
    resolve_func : Callable[[ActionContext], ExecutionResult] = no_result_function
    wf_finished  : bool = False
    name         : StepName = field(default=StepName.RESOLVE, init=False)


@dataclass
class InitStepConfig(AutomaticStepConfig):
    name          : StepName = field(default=StepName.INIT, init=False)
    wf_name       : WorkflowName | None = None
    decision_func : Callable[[ActionContext], WorkflowConfig] | None = None
    wf_config     : WorkflowConfig | None = None
    as_child      : bool = True

A = TypeVar("A", bound=UserAction)
T = TypeVar("T")
@dataclass 
class SetStepConfig(AutomaticStepConfig, Generic[A]):
    getter          : Callable[[A], T]
    setter          : Callable[[WorkflowData, T], None]
    name            : StepName = field(default=StepName.SET, init=False)

@dataclass
class RepeatStepConfig(AutomaticStepConfig):
    @staticmethod
    def no_check_func(ctx : ActionContext) -> bool:
        return True
    
    name                : StepName = field(default=StepName.REPEAT, init=False)
    repeat_from_index   : int = 0
    check_func          : Callable[[ActionContext], bool] = no_check_func