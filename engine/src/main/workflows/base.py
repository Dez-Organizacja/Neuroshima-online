from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from main.state.contex import ActionContext
from main.steps.factory import StepFactory
from main.rules.workflow.base import WorkflowRules
R = TypeVar("R", bound=WorkflowRules)


class Workflow(ABC, Generic[R]):
    def __init__(self, rules : R):
        super().__init__()
        self.rules = rules
        self.steps_list = self.build_steps()

    @abstractmethod
    def build_steps(self):
        pass

    @classmethod
    def get_first_step_index(cls, ctx : ActionContext):
        return 0

    @staticmethod
    def advance(ctx : ActionContext):
        ctx.workflow_instance.current_step_index += 1

    def finished(self, ctx : ActionContext) -> bool:
        return len(self.steps_list) > ctx.workflow_instance.current_step_index

    def get_current_step(self, ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        return StepFactory.create(config=self.steps_list[idx])