from abc import ABC, abstractmethod
from main.state.contex import ActionContext
from main.input.data import UserAction

from main.steps.config import (
    StepName, 
    StepConfig,
    ResolveStepConfig,
    InitStepConfig,
    WaitingStepConfig,
    SetStepConfig,
    RepeatStepConfig
)

from main.events.workflow import PopWorkflow, PushWorkflow, GoToStep
from main.events.data import ExecutionResult
from main.steps.data import StepResult

from typing import TypeVar, Generic

C = TypeVar("C", bound=StepConfig)

class Step(ABC, Generic[C]):
    def __init__(self, config : C):
        self.name : StepName = config.name
        self.config : C = config

    @abstractmethod
    def execute(self, 
                ctx : ActionContext,
                action : UserAction | None = None 
        ) -> StepResult:
        return StepResult()

    @property
    def requires_input(self) -> bool:
        return self.name == StepName.WAITING

class WaitingStep(Step[WaitingStepConfig]):
    def __init__(self, config : WaitingStep):
        super().__init__(config)

    def execute(self, ctx : ActionContext, action = None) -> StepResult:
        result = self.config.action_handler.handle(ctx, action)
        return StepResult(
            execution_result=result,
            input_consumed=self.config.consume_action
        )

class AutomaticStep(Step[C], ABC):
    def __init__(self, config : C):
        super().__init__(config)
        
    @abstractmethod
    def execute(self, ctx : ActionContext) -> StepResult:
        pass


class ResolveStep(AutomaticStep[ResolveStepConfig]):
    def __init__(self, config : ResolveStepConfig):
        super().__init__(config)

    @staticmethod
    def no_resolve_func(ctx : ActionContext):
        return ExecutionResult()
    
    def execute(self, ctx : ActionContext) -> StepResult:
        res = ExecutionResult(action_result=self.config.resolve_func(ctx))
        if self.config.wf_finished:
            res.workflow_effects = [PopWorkflow()]
        return StepResult(execution_result=res)


A = TypeVar("A", bound = UserAction)
   
class SetStep(AutomaticStep[SetStepConfig], Generic[A]):
    def __init__(self, config : SetStepConfig, action : A):
        super().__init__(config)
        self.action = action

    def execute(self, ctx : ActionContext) -> StepResult:
        value = self.config.getter(self.action)
        self.config.setter(ctx.workflow_data, value)
        return StepResult()

class InitStep(AutomaticStep[InitStepConfig]):
    def __init__(self, config : InitStepConfig):
        super().__init__(config)

    def execute(self, ctx : ActionContext) -> StepResult:
        effect = PushWorkflow(
            name=self.name or self.config.decision_func(ctx),
            as_child=self.config.as_child,
            config = self.config
        )
        return StepResult(
            execution_result=ExecutionResult(workflow_effects=[effect])
        ) 
    
class RepeatStep(AutomaticStep[RepeatStepConfig]):
    def __init__(self, config : RepeatStepConfig):
        super().__init__(config)

    def execute(self, ctx : ActionContext) -> StepResult:
        res = StepResult()
        if self.config.check_func(ctx):
            effect = GoToStep(self.config.repeat_from_index)
            res.execution_result.workflow_effects.append(effect)
            res.advance = False
            
        return res