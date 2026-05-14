from main.workflows.data import WorkflowName
from main.workflows.move import MoveWorkflow
from main.workflows.push import PushWorkflow
from main.workflows.data import WorkflowInstance, ABILITY_WORKFLOW_REGISTRY
from main.workflows.base import Workflow
from main.tokens.data import Ability

class WorkflowFactory:
    WORKFLOWS : dict[WorkflowName, Workflow] = {
        WorkflowName.MOVE : MoveWorkflow,
        WorkflowName.PUSH : PushWorkflow,
    }
    @classmethod
    def create(cls, workflow_name : WorkflowName):
        workflow_name = WorkflowName(workflow_name)
        return cls.WORKFLOWS[workflow_name]()

    @classmethod
    def get_workflow_instance(cls, 
                              workflow_name : WorkflowName, 
                              source : WorkflowName
        ):
        workflow_name = WorkflowName(workflow_name)
        wf = cls.WORKFLOWS[workflow_name]
        return WorkflowInstance(
            name = workflow_name,
            current_step_index=wf.get_first_step_index(source)
        )
    
    @classmethod
    def get_workflow_for_ability(cls, ability_name : Ability):
        return cls.create(ABILITY_WORKFLOW_REGISTRY[ability_name])
