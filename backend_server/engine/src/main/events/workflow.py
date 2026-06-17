from dataclasses import dataclass, field
from main.state.context import ActionContext
from main.events.data import WorkflowEvent, OnClickData
from main.workflows.data import WorkflowConfig, WorkflowName, WorkflowInstance
from typing import Callable

@dataclass
class PushWorkflow(WorkflowEvent):
    name: WorkflowName
    as_child: bool = True
    config: WorkflowConfig = field(default_factory=WorkflowConfig)
    # def __post_init__(self):
    #     print(f"CREATING PUSH WORKFLOW {self.name}")

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
    # def __init__(cls):
    #     print(f"INITIALINIG POPWORKFLOW")

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
        print(f"DELETE ABOVE {self.name}")
        while ctx.workflow_instance.name != self.name:
            ctx.state.workflow_stack.pop(-1)
        
@dataclass
class ConsumeOnClick(WorkflowEvent):
    name : WorkflowName

    def apply(self, ctx : ActionContext):
        for instance in ctx.state.workflow_stack:
            if instance.name != self.name:
                continue

            instance.on_click_consumed = True
            return
        # ctx.workflow_instance.on_click_consumed = True
        raise ValueError(f"no workflow {self.name} on workflow stack")


@dataclass
class SetActionHook(WorkflowEvent):
    effects : OnClickData
    name : WorkflowName

    def apply(self, ctx : ActionContext):
        # print("SET ACTION HOOK")
        for instance in ctx.state.workflow_stack:
            if instance.name != self.name:
                continue

            instance.on_click = self.effects
            return
        raise ValueError(f"no workflow {self.name} on workflow stack")

@dataclass
class EnqueueWorkflow(WorkflowEvent):
    name : WorkflowName
    config : WorkflowConfig

    def apply(self, ctx : ActionContext):
        ctx.state.pending_workflows.append(
            WorkflowInstance(
                name=self.name,
                config=self.config 
            )
        )

@dataclass
class PopAllWorkflows(WorkflowEvent):
    def apply(self, ctx : ActionContext):
        ctx.state.workflow_stack.clear()