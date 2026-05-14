from abc import ABC, abstractmethod

from main.state.contex import ActionContext
from main.state.user_action import UserAction

from main.workflows.data import WorkflowName
from main.workflows.factory import WorkflowFactory

from main.actions.exeute_actions.action_result import ActionResult
from main.actions.available_actions.available_action_result import AvailableActionResult

from main.steps.config import (
    StepType, 
    InputStepConfig,
    ResolveStepConfig,
    AutomaticStepConfig,
    InitStepConfig,
    DecisionStepConfig
)
from main.steps.result import StepResult

class Step(ABC):
    def __init__(self, type: StepType, config = None):
        self.type = type
        self.config = config

    @abstractmethod
    def execute(self, 
                ctx : ActionContext,
                action : UserAction | None = None 
        ):
        pass

    @property
    def requires_input(self):
        return self.type in (StepType.INPUT, StepType.CHOICE)

class InputStep(Step):
    def __init__(self, config : InputStepConfig):
        super().__init__(StepType.INPUT, config)
        self.config : InputStepConfig = config

    def execute(self, ctx : ActionContext, action : UserAction):
        value = self.config.getter(action)
        self.config.setter(ctx.workflow_data, value)
        return StepResult(input_consumed=self.config.consume_action)

    def get_available_actions(self, ctx : ActionContext):
        return AvailableActionResult(
            positions= self.config.get_positions(ctx),
            bottoms=self.config.allowed_bottoms,
            hand=self.config.get_available_tokens(ctx)
        )

class AutomaticStep(Step, ABC):
    def __init__(self, config : AutomaticStepConfig):
        super().__init__(StepType.AUTOMATIC, config)
        
    @abstractmethod
    def execute(self, ctx : ActionContext):
        pass
    

class ResolveStep(AutomaticStep):
    def __init__(self, config : ResolveStepConfig = None):
        super().__init__(config)
        if config:
            self.resolve_func = config.resolve_func
            self.wf_finished = config.wf_finished
        else:
            self.resolve_func = self.no_resolve_func
            self.wf_finished = False

    @staticmethod
    def no_resolve_func(ctx : ActionContext):
        return ActionResult()
    
    def execute(self, ctx : ActionContext):
        return StepResult(
            action_result=self.resolve_func(ctx),
            pop_workflow=self.wf_finished
        )
    
class InitStep(AutomaticStep):
    def __init__(self, config : InitStepConfig):
        super().__init__(config)
        self.decision_func = config.decision_func

    def execute(self, ctx : ActionContext):
        new_workflow_name = self.decision_func(ctx)
        current_workflow_name = ctx.workflow_instance.name
        instance = WorkflowFactory.get_workflow_instance(
            workflow_name=new_workflow_name,
            source=current_workflow_name
        )
        if self.config.as_child:
            return StepResult(push_workflow=instance)
        else:
            return StepResult(replace_workflow=instance)