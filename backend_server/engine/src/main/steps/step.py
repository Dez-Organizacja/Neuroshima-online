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
from main.events.data import Event
from main.steps.data import StepResult
from main.systems.on_click import OnClickSystem

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
    @abstractmethod
    def requires_input(self) -> bool:
        pass

    def can_skip(self, ctx : ActionContext) -> bool:
        return False

class WaitingStep(Step[WaitingStepConfig]):
    def __init__(self, config : WaitingStepConfig):
        super().__init__(config)

    def can_skip(self, ctx : ActionContext) -> bool:
        return self.config.can_skip(ctx)

    def execute(self, ctx : ActionContext, action : UserAction) -> StepResult:
        # print("WAITING STEP")
        self.config.action_handler.handle(ctx, action)
        # print(f"wf instance {ctx.workflow_instance}")
        result = OnClickSystem.resolve(ctx.workflow_instance)
        # print(f"result: {result}")
        # print(f"workflow data {ctx.workflow_data}")
        return StepResult(execution_result=result)
    
    @property
    def requires_input(self):
        return True

class AutomaticStep(Step[C], ABC):
    def __init__(self, config : C):
        super().__init__(config)
        
    @abstractmethod
    def execute(self, ctx : ActionContext) -> StepResult:
        pass

    @property
    def requires_input(self):
        return False

class ResolveStep(AutomaticStep[ResolveStepConfig]):
    def __init__(self, config : ResolveStepConfig):
        super().__init__(config)
    
    def execute(self, ctx : ActionContext) -> StepResult:
        # print(f"EXECUTING RESOLVE STEP")
        res : list[Event] = self.config.resolve_func(ctx) or []
        # print("FINISHED CONFIG FUNCTION RESOLVING")
        if self.config.wf_finished:
            res.append(PopWorkflow())
        #     print("finished workflow effect pushed")
        # print("FINISHED EXECUTING RESOLVE STEP")
        return StepResult(execution_result=res)


A = TypeVar("A", bound = UserAction)
   
# class SetStep(AutomaticStep[SetStepConfig], Generic[A]):
#     def __init__(self, config : SetStepConfig, action : A):
#         super().__init__(config)
#         self.action = action

#     def execute(self, ctx : ActionContext) -> StepResult:
#         value = self.config.getter(self.action)
#         self.config.setter(ctx.workflow_data, value)
#         return StepResult()

class InitStep(AutomaticStep[InitStepConfig]):
    def __init__(self, config : InitStepConfig):
        super().__init__(config)

    def execute(self, ctx : ActionContext) -> StepResult:
        # print("executing init workflow step")
        # print(f"decision function {self.config.decision_func}")
        effect = PushWorkflow(
            name=self.config.wf_name or self.config.decision_func(ctx),
            as_child=self.config.as_child,
            config = self.config.wf_config
        )
        return StepResult(execution_result=[effect]) 
    
class RepeatStep(AutomaticStep[RepeatStepConfig]):
    def __init__(self, config : RepeatStepConfig):
        super().__init__(config)

    def execute(self, ctx : ActionContext) -> StepResult:
        res = StepResult()
        if self.config.check_func(ctx):
            effect = GoToStep(self.config.repeat_from_index)
            res.execution_result.append(effect)
            res.advance = False
            
        return res