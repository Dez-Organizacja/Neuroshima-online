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
from main.workflows.headquarter import HeadquarterTurnWorkflow
from main.workflows.dispatch import HandWorkflow, BoardWorkflow
from main.workflows.turn import TurnWorkflow
from main.workflows.data import WorkflowInstance, WorkflowName
from main.workflows.start_battle import StartBattleWorkflow
from main.workflows.healers import HealersWorkflow
from main.workflows.battle import BattleWorkflow
from main.workflows.explosion import ExpolsionWorkflow
from main.workflows.initiative import InitiativeWorkflow
from main.workflows.damage_resolve import ResolveDamageWorkflow
from main.workflows.end_turn_confirm import EndTurnConfirmWorkflow
from main.workflows.draw import DrawWorkflow
from main.workflows.endgame import EndGameSequenceWorkflow
from main.workflows.game_over import GameOverWorkflow
from main.workflows.action import AcitonWorkflow
from main.workflows.end_action import EndActionWorkflow
from main.workflows.movement import MovementWorkflow
from main.workflows.base import Workflow
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
        WorkflowName.START_BATTLE : WorkflowMeta(StartBattleWorkflow, False),
        WorkflowName.GAMEOVER : WorkflowMeta(GameOverWorkflow, False),
        WorkflowName.ACTION : WorkflowMeta(AcitonWorkflow, False),
        WorkflowName.END_ACTION : WorkflowMeta(EndActionWorkflow, False),
        WorkflowName.END_TURN_CONFIRM : WorkflowMeta(EndTurnConfirmWorkflow, False),
        WorkflowName.MOVEMENT : WorkflowMeta(MovementWorkflow, False),

        #configurable workflows
        WorkflowName.TURN : WorkflowMeta(TurnWorkflow, True),
        WorkflowName.GAME : WorkflowMeta(GameWorkflow, True),
        WorkflowName.HEAL : WorkflowMeta(HealersWorkflow, True),
        WorkflowName.HEADQUARTER_TURN : WorkflowMeta(HeadquarterTurnWorkflow, True),
        WorkflowName.BATTLE : WorkflowMeta(BattleWorkflow, True),
        WorkflowName.HEAL   : WorkflowMeta(HealersWorkflow, True),
        WorkflowName.TURN   : WorkflowMeta(TurnWorkflow, True),
        WorkflowName.GAME   : WorkflowMeta(GameWorkflow, True),
        WorkflowName.EXPLOSION : WorkflowMeta(ExpolsionWorkflow, True),
        WorkflowName.INITIATIVE : WorkflowMeta(InitiativeWorkflow, True),
        WorkflowName.DAMAGE_RESOLVE : WorkflowMeta(ResolveDamageWorkflow, True),
        WorkflowName.DRAW : WorkflowMeta(DrawWorkflow, True),
        WorkflowName.ENDGAMESEQUENCE : WorkflowMeta(EndGameSequenceWorkflow, True),
    }
    @classmethod
    def create(cls, instance : WorkflowInstance) -> Workflow:
        meta = cls.WORKFLOWS[instance.name]
        if meta.needs_config:
            return meta.cls(instance.config)
        else:
            return meta.cls()
