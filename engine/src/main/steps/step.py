from abc import ABC, abstractmethod

from main.state.contex import ActionContext
from main.state.user_action import UserAction

from main.workflows.data import WorkflowName, WorkflowConfig
from main.workflows.factory import WorkflowFactory

from main.actions.execute.result import ActionResult
from main.actions.available.result import AvailableActionResult

from main.steps.config import (
    StepName, 
    StepConfig,
    ResolveStepConfig,
    InitStepConfig,
    WaitingStepConfig,
    SetStepConfig,
    EndTurnChcekConfig
)
from main.steps.data import StepResult
from main.events.workflow import PopWorkflow, PushWorkflow, GoToStep

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
        ):
        return StepResult()

    @abstractmethod
    def get_available_actions(self, ctx : ActionContext):
        return AvailableActionResult()

    @property
    def requires_input(self):
        return self.name == StepName.WAITING

class WaitingStep(Step[WaitingStepConfig]):
    def __init__(self, config : WaitingStep):
        super().__init__(config)

    def execute(self, ctx : ActionContext, action = None):
        return StepResult(input_consumed=True)
    
    def get_available_actions(self, ctx : ActionContext):
        return AvailableActionResult(
            positions=self.config.get_positions(ctx),
            bottoms=self.config.get_bottoms(ctx),
            hand=self.config.get_tokens(ctx),
        )

class AutomaticStep(Step[C], ABC):
    def __init__(self, config : C):
        super().__init__(config)
        
    @abstractmethod
    def execute(self, ctx : ActionContext):
        pass

    def get_available_actions(self, ctx : ActionContext):
        return super().get_available_actions(ctx)
    

class ResolveStep(AutomaticStep[ResolveStepConfig]):
    def __init__(self, config : ResolveStepConfig):
        super().__init__(config)

    @staticmethod
    def no_resolve_func(ctx : ActionContext):
        return ActionResult()
    
    def execute(self, ctx : ActionContext):
        res = StepResult(action_result=self.config.resolve_func(ctx))
        if self.config.wf_finished:
            res.workflow_effects = [PopWorkflow()]
        return res

A = TypeVar("A", bound = UserAction)
   
class SetStep(AutomaticStep[SetStepConfig], Generic[A]):
    def __init__(self, config : SetStepConfig, action : A):
        super().__init__(config)
        self.action = action

    def execute(self, ctx : ActionContext):
        value = self.config.getter(self.action)
        self.config.setter(ctx.workflow_data, value)

class InitStep(AutomaticStep[InitStepConfig]):
    def __init__(self, config : InitStepConfig):
        super().__init__(config)

    def execute(self, ctx : ActionContext):
        wf_name = self.config.wf_name or self.config.decision_func(ctx)
        return StepResult(
            workflow_effects=[PushWorkflow(
                name=wf_name,
                as_child=self.config.as_child,
            )]
        )
    
class EndTurnChcekStep(AutomaticStep[EndTurnChcekConfig]):
    def __init__(self, config : EndTurnChcekConfig):
        super().__init__(config)

    def execute(self, ctx : ActionContext):
        res = StepResult()
        if self.config.check_func(ctx):
            res.workflow_effects.append(PopWorkflow())
            res.action_result = self.config.resolve_func(ctx)

        else:
            res.workflow_effects.append(GoToStep(self.config.repeat_from_index))
            res.advance = False