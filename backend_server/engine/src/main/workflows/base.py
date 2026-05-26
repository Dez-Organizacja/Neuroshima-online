from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from main.state.contex import ActionContext
from main.steps.factory import StepFactory
from main.workflows.providers.base import WorkflowActionProvider
from main.steps.step import Step

P = TypeVar("R", bound=WorkflowActionProvider)

class Workflow(ABC, Generic[P]):
    def __init__(self, action_provider : P | None = None):
        self.action_provider : P = action_provider or WorkflowActionProvider()
        self.steps_list = []

    @abstractmethod
    def _build_steps(self):
        pass

    def build_steps(self):
        self.steps_list = self._build_steps()

    def start(self, ctx : ActionContext):
        ctx.workflow_instance.current_step_index = self.get_first_step_index(ctx)

    def get_first_step_index(self, ctx : ActionContext):
        return 0

    def get_current_step(self, ctx : ActionContext) -> Step:
        idx = ctx.workflow_instance.current_step_index
        return StepFactory.create(config=self.steps_list[idx])