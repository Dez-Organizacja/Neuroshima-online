from main.steps.config import (
    ResolveStepConfig,
    WaitingStepConfig,
    InitStepConfig,
    RepeatStepConfig,
)
from main.workflows.data import WorkflowData, WorkflowName, WorkflowConfig
from main.state.contex import ActionContext
from main.events.data import Event
from main.events.effects import ClearWorkflowDataEffect
from main.events.flow import CheckGameOverEvent, GameOverEvent
from main.events.workflow import PopWorkflow, PushWorkflow
from main.input.action_handlers import ActionHandler
from typing import Callable

resolve_func_type = Callable[[ActionContext], list[Event]]
class StepBuilderMixin:
    def build_end_step(self, *funcs : resolve_func_type):
        return self.build_resolve_step(*funcs, finish=True)
    
    @staticmethod
    def build_resolve_step(*funcs : resolve_func_type, finish : bool = False):
        def resolve_func(ctx : ActionContext) -> list[Event]:
            # print("RESOLVING RESOLVE FUNCTIONS")
            result = []
            for func in funcs:
                # print(f"RESOLVING FUNCTION {func}")
                events = func(ctx)
                # print("CHECKING RESULT EVENTS")
                if events:
                    result.extend(events)
            return result
        
        return ResolveStepConfig(resolve_func, wf_finished=finish)

    def build_end_game_check_step(self):
        return self.build_resolve_step(lambda ctx : [CheckGameOverEvent()])

    def build_end_game_step(self):
        return self.build_resolve_step(lambda ctx : [GameOverEvent()])

    @staticmethod
    def build_input_step(
        setter = None, 
        can_skip : Callable[[ActionContext], bool] | None = None,
        message : str = "",
    ):
        can_skip = can_skip or (lambda ctx : False)
        return WaitingStepConfig(
            ActionHandler(setter=setter),
            can_skip=can_skip,
            message=message,
        )
    
    @staticmethod
    def build_push_workflow_step(name : WorkflowName, config : WorkflowConfig | None = None):
        config = config or WorkflowConfig()
        return InitStepConfig(wf_name=name, wf_config=config)
    
    @staticmethod
    def build_dispatch_step(
        dispatch_function : Callable[[ActionContext], WorkflowName]
    ) -> InitStepConfig:
        return InitStepConfig(decision_func=dispatch_function)

    @staticmethod
    def build_repeat_step(
        index : int = 0,
        func : Callable[[ActionContext], bool] | None = None,
    ) -> RepeatStepConfig:
        if func:
            return RepeatStepConfig(repeat_from_index=index, check_func=func)
        return RepeatStepConfig(repeat_from_index=index)

    
    def build_check_workflow_break_step(
            self, 
            predicate_func : Callable[[ActionContext], bool],
            finish_func : Callable[[ActionContext], list[Event]] | None = None,
        ):
        finish_func = finish_func or (lambda ctx : [])
        def resolve_func(ctx : ActionContext):
            if predicate_func(ctx):
                return [
                    *finish_func(ctx),
                    PopWorkflow()
                ]
        return self.build_resolve_step(resolve_func)
    
    @staticmethod
    def push_workflow(name : WorkflowName, config : WorkflowConfig | None = None):
        config = config or WorkflowConfig()
        return [PushWorkflow(name=name, config=config)]

    @staticmethod
    def clear_wf_data(ctx : ActionContext):
        return [ClearWorkflowDataEffect()]

class BoardSelectionMixin(StepBuilderMixin):
    def build_source_step(self, message : str = ""):
        return self.build_input_step(WorkflowData.set_unit_pos, message=message)

    def build_destination_step(self, message : str = ""):
        return self.build_input_step(WorkflowData.set_destination, message=message)
    
    def build_target_step(self, message : str = ""):
        return self.build_input_step(WorkflowData.set_target_pos, message=message)
