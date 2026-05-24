from main.state.contex import ActionContext
from main.events.data import WorkflowEvent
from main.workflows.data import WorkflowConfig, WorkflowName, WorkflowInstance

class PushWorkflow(WorkflowEvent):
    def __init__(self,
                 name : WorkflowName,
                 as_child : bool = True,
                 config : WorkflowConfig | None = None
        ):
        super().__init__()
        self.name = name
        self.as_child = as_child
        self.config = config

    def apply(self, ctx : ActionContext):
        wf_instance = WorkflowInstance(
            name = self.name,
            config = self.config
        )
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

class DeleteAbove(WorkflowEvent):
    def __init__(self, name : WorkflowName):
        self.name : WorkflowName = name
    
    def apply(self, ctx : ActionContext):
        while ctx.workflow_instance.name != self.name:
            ctx.state.workflow_stack.pop(-1)
        