from dataclasses import dataclass, field
from main.state.contex import ActionContext
from main.events.data import WorkflowEvent
from main.workflows.data import WorkflowConfig, WorkflowName, WorkflowInstance


@dataclass
class PushWorkflow(WorkflowEvent):
    name: WorkflowName
    as_child: bool = True
    config: WorkflowConfig = field(default_factory=WorkflowConfig)

    def apply(self, ctx: ActionContext):
        wf_instance = WorkflowInstance(
            name=self.name,
            config=self.config,
        )
        print(f"PUSH {self.name}")
        # print(self.name)
        # print(self.config)
        if self.as_child:
            ctx.state.workflow_stack.append(wf_instance)
        else:
            ctx.state.workflow_stack[-1] = wf_instance


@dataclass
class PopWorkflow(WorkflowEvent):
    def apply(self, ctx: ActionContext):
        print(f"POPWORKFLOW {ctx.workflow_instance.name}")
        ctx.state.workflow_stack.pop(-1)


@dataclass
class GoToStep(WorkflowEvent):
    index: int

    def apply(self, ctx: ActionContext):
        ctx.workflow_instance.current_step_index = self.index


@dataclass
class DeleteAbove(WorkflowEvent):
    name: WorkflowName

    def apply(self, ctx: ActionContext):
        # print(f"DELETE ABOVE {self.name}")
        while ctx.workflow_instance.name != self.name:
            ctx.state.workflow_stack.pop(-1)
        
@dataclass
class ConsumeOnClick(WorkflowEvent):
    def apply(self, ctx : ActionContext):
        ctx.workflow_instance.on_click_consumed = True