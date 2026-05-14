from abc import ABC, abstractmethod
from main.state.contex import ActionContext
from main.steps.factory import StepFactory
from main.workflows.data import WorkflowName, ABILITY_WORKFLOW_REGISTRY
from main.rules.workflow.base import WorkflowRules
from main.tokens.data import Ability

class Workflow(ABC):
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

    def advance(self, ctx : ActionContext):
        ctx.workflow_instance.current_step_index += 1

    def get_current_step(self, ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        return StepFactory.create(config=self.steps_list[idx])
    
    def next_workflow_maker(self, name : WorkflowName):
        def function(ctx : ActionContext):
            return name
        return function
    
    def get_workflow_for_ability(self, ability : Ability) -> WorkflowName:
        return ABILITY_WORKFLOW_REGISTRY[ability]
    
    def get_active_token(self, ctx : ActionContext):
        return None