from abc import ABC, abstractmethod
from main.state.contex import ActionContext
from main.steps.factory import StepFactory
from main.workflows.data import WorkflowName, ABILITY_WORKFLOW_REGISTRY
from main.rules.workflow.base import WorkflowRules
from main.tokens.data import Ability
from typing import TypeVar, Generic

R = TypeVar("R", bound=WorkflowRules)


class Workflow(ABC, Generic[R]):
    def __init__(self, rules : WorkflowRules):
        super().__init__()
        self.rules = rules
        self.steps_list = self.build_steps()

    @abstractmethod
    def build_steps(self):
        pass

    @classmethod
    def get_first_step_index(cls, source : WorkflowName):
        return 0

    @staticmethod
    def advance(ctx : ActionContext):
        ctx.workflow_instance.current_step_index += 1

    def get_current_step(self, ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        return StepFactory.create(config=self.steps_list[idx])
    
    @staticmethod
    def next_workflow_maker(name : WorkflowName):
        def function(ctx : ActionContext):
            return name
        return function
    
    @staticmethod
    def get_workflow_for_ability(ability : Ability) -> WorkflowName:
        return ABILITY_WORKFLOW_REGISTRY[ability]
    
    @staticmethod
    def get_active_token(ctx : ActionContext):
        return None