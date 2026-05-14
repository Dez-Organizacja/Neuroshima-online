from abc import ABC, abstractmethod
from main.workflows.base import Workflow
from main.rules.workflow.base import WorkflowRules
from main.state.contex import ActionContext
from main.steps.config import InputStepConfig, ResolveStepConfig
from main.state.user_action import BoardAction
from main.workflows.data import WorkflowData
from main.actions.exeute_actions.action_result import ActionResult

class TargetWorkflow(Workflow, ABC):
    def __init__(self, rules : WorkflowRules):
        super().__init__(rules)

    @abstractmethod
    def get_available_targets(self, ctx : ActionContext):
        pass

    @abstractmethod
    def get_available_bottoms(self, ctx : ActionContext):
        pass

    @abstractmethod
    def resolve_func(self, ctx : ActionContext) -> ActionResult:
        pass

    def build_target_step(self):
        return InputStepConfig(
            getter = BoardAction.get_pos,
            setter = WorkflowData.set_target_pos,
            get_positions = self.get_available_targets,
            get_bottoms = self.get_available_bottoms
        )


    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func = self.resolve_func,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_target_step(),
            self.build_end_step()
        ]