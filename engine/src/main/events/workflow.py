from main.state.contex import ActionContext
from main.events.data import Event
from main.workflows.data import WorkflowName
from main.workflows.factory import WorkflowFactory
from abc import ABC

class WorkflowEvent(Event, ABC):
    pass

class PushWorkflow(WorkflowEvent):
    def __init__(self,
                 name : WorkflowName,
                 as_child : bool = True
        ):
        super().__init__()
        self.name = name
        self.as_child = as_child

    def apply(self, ctx : ActionContext):
        wf_instance = WorkflowFactory.get_workflow_instance(self.config.name)
        if self.as_child:
            ctx.state.workflow_stack.append(wf_instance)
        else:
            ctx.state.workflow_stack[-1] = wf_instance

class PopWorkflow(WorkflowEvent):
    def apply(self, ctx : ActionContext):
        ctx.state.workflow_stack.pop(-1)

class GoToStep(WorkflowEvent):
    def __init__(self, index):
        self.index = index
    
    def apply(self, ctx : ActionContext):
        ctx.workflow_instance.current_step_index = self.index