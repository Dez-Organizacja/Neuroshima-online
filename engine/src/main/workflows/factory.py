from main.workflows.move import MoveWorkflow
from main.workflows.push import PushWorkflow
from main.workflows.placement import PlaceWorkflow
from main.workflows.rotate import RotateWorkflow
from main.workflows.target import (
    SniperWorkflow, 
    BombWorkflow, 
    GranadeWorkflow
)
from main.workflows.game import GameWorkflow
from main.workflows.dispatch import HandWorkflow, BoardWorkflow
from main.workflows.turn import TurnWorkflow
from main.workflows.data import WorkflowInstance, WorkflowName, WorkflowConfig
from main.workflows.base import Workflow
from main.state.contex import ActionContext
from dataclasses import dataclass

@dataclass
class WorkflowMeta:
    cls : type[Workflow]
    needs_config : bool

class WorkflowFactory:
    WORKFLOWS : dict[WorkflowName, type[WorkflowMeta]] = {
        WorkflowName.MOVE : WorkflowMeta(MoveWorkflow, False),
        WorkflowName.PUSH : WorkflowMeta(PushWorkflow, False),
        WorkflowName.PLACE : WorkflowMeta(PlaceWorkflow, False),
        WorkflowName.ROTATE : WorkflowMeta(RotateWorkflow, False),
        WorkflowName.SNIPER : WorkflowMeta(SniperWorkflow, False),
        WorkflowName.BOMB : WorkflowMeta(BombWorkflow, False),
        WorkflowName.GRENADE : WorkflowMeta(GranadeWorkflow, False),
        WorkflowName.HAND : WorkflowMeta(HandWorkflow, False),
        WorkflowName.BOARD : WorkflowMeta(BoardWorkflow, False),
        WorkflowName.TURN : WorkflowMeta(TurnWorkflow, True),
        WorkflowName.GAME : WorkflowMeta(GameWorkflow, True)
    }
    @classmethod
    def create(cls, config : WorkflowConfig) -> Workflow:
        meta = cls.WORKFLOWS[config.name]
        if meta.needs_config:
            return meta.cls(config)
        else:
            return meta.cls()

    @classmethod
    def get_workflow_instance(cls, 
                              config : WorkflowConfig, 
                              ctx : ActionContext
        ) -> WorkflowInstance:
        wf_cls = cls.WORKFLOWS[config.name].cls
        return WorkflowInstance(
            config=config,
            current_step_index=wf_cls.get_first_step_index(ctx)
        )
