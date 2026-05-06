from abc import ABC, abstractmethod
from main.workflows.data import WorkflowSource
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.steps.step import Step

class Workflow(ABC):
    def __init__(self, rules):
        super().__init__()
        self.rules = rules
        self.steps_list = self.build_steps()
        
    def start(cls, 
              ctx : ActionContext, 
              workflow_source : WorkflowSource | None =  None
        ):
        ctx.workflow_data = WorkflowData(workflow_source)

    @abstractmethod
    def build_steps(self):
        pass

    @abstractmethod
    def finish(self, ctx : ActionContext): 
        pass
   
    def get_sources(self, ctx : ActionContext):
        return self.rules.get_available_sources(ctx)
    
    def get_targets(self, ctx : ActionContext):
        return self.rules.get_available_targets(ctx)
    
    def get_destinations(self, ctx : ActionContext):
        return self.rules.get_available_destinations(ctx)


    def advance(self, ctx : ActionContext):
        ctx.workflow_data.current_step_index += 1
        if ctx.workflow_data.current_step_index >= len(self.steps_list):
            return self.finish(ctx)

    def get_current_step(self, ctx : ActionContext):
        idx = ctx.workflow_data.current_step_index
        return Step(config=self.steps_list[idx])