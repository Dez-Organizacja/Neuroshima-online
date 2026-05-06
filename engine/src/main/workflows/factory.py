from main.workflows.data import WorkflowName
from main.workflows.move import MoveWorkflow
from main.workflows.push import PushWorkflow
from main.workflows.choosing_action import ChoosingActionWorkflow

class WorkflowFactory:
    WORKFLOWS = {
        WorkflowName.MOVE : MoveWorkflow,
        WorkflowName.PUSH : PushWorkflow,
        WorkflowName.CHOOSING_ACTION : ChoosingActionWorkflow
    }
    @classmethod
    def create(cls, workflow_name : WorkflowName):
        return cls.WORKFLOWS[workflow_name]()