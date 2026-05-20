from main.workflows.move import MoveWorkflow
from main.workflows.push import PushWorkflow
from main.workflows.data import WorkflowInstance, WorkflowName
from main.workflows.base import Workflow
from main.state.contex import ActionContext

class WorkflowFactory:
    WORKFLOWS : dict[WorkflowName, Workflow] = {
        WorkflowName.MOVE : MoveWorkflow,
        WorkflowName.PUSH : PushWorkflow,
    }
    @classmethod
    def create(cls, name : WorkflowName):
        return cls.WORKFLOWS[name]()

    @classmethod
    def get_workflow_instance(cls, name : WorkflowName, ctx : ActionContext):
        wf = cls.WORKFLOWS[name]
        return WorkflowInstance(
            name = name,
            current_step_index=wf.get_first_step_index(ctx)
        )
