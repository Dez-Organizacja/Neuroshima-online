from dataclasses import dataclass, field
from main.events.data import FlowEvent, Event
from main.events.workflow import PushWorkflow, PopWorkflow, DeleteAbove, EnqueueWorkflow, PopAllWorkflows
from main.events.effects import ResetAbilityUsedEffect
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName, WorkflowConfig
from main.utils.variable import Phase

@dataclass
class SetActiveFaction(FlowEvent):
    faction : str = ""
    # def __post_init__(self):
        # print(f"CREATED SET ACTIVE FACTION {self.faction}")

    def apply(self, ctx : ActionContext) -> list[Event]:
        # print("CHAGING ACTIVE FACTION")
        ctx.faction = self.faction

@dataclass
class SetGamePahseEvent(FlowEvent):
    phase : Phase
    
    def apply(self, ctx : ActionContext):
        ctx.state.phase = self.phase

@dataclass
class StartTurnEvent(FlowEvent):
    faction : str
    positions : list[tuple[int, int]] = field(default_factory=list)

    def apply(self, ctx : ActionContext):
        ctx.state.turn_faction = self.faction
        return [
            SetActiveFaction(faction=self.faction),
            ResetAbilityUsedEffect(self.positions),
        ]

@dataclass
class EndTurnEvent(FlowEvent):
    turn_name : WorkflowName = WorkflowName.TURN
    next_workflow : PushWorkflow | None = None

    def apply(self, ctx: ActionContext) -> list[Event]:
        ctx.state.turn_faction = ""
        effects = [
            SetActiveFaction(faction=""),
            DeleteAbove(name=self.turn_name),
            PopWorkflow(),
        ]
        if self.next_workflow is not None:
            effects.append(self.next_workflow)
        return effects

@dataclass
class StartBattleEvent(FlowEvent):
    def apply(self, ctx: ActionContext) -> list[Event]:
        battle_workflow = PushWorkflow(
            name=WorkflowName.BATTLE,
            config=WorkflowConfig(factions=ctx.state.factions)
        )
        return [EndTurnEvent(next_workflow=battle_workflow)]
    
@dataclass
class BuildEndGameWorkflowEvent(FlowEvent):
    faction: str

    def apply(self, ctx: ActionContext) -> list[Event]:
        enemy = ctx.rules.get_enemy(ctx.state.factions, self.faction)

        return [
            EnqueueWorkflow(
                name=WorkflowName.ENDGAMESEQUENCE,
                config=WorkflowConfig(
                    factions=[self.faction, enemy]
                )
            )
        ]

@dataclass
class EndGameSequenceEvent(FlowEvent):
    faction : str
    
    def apply(self, ctx : ActionContext):
        return [
            SetGamePahseEvent(Phase.ENDGAME),
            BuildEndGameWorkflowEvent(self.faction),
        ]

@dataclass 
class TriggerEndGameSequenceEvent(FlowEvent):
    def apply(self, ctx : ActionContext):
        if ctx.player.pile.empty and ctx.phase != Phase.ENDGAME:
            return [EndGameSequenceEvent(ctx.faction)]

@dataclass
class GameOverEvent(FlowEvent):
    def apply(self, ctx : ActionContext) -> list[Event]:
        return [
            SetGamePahseEvent(Phase.GAMEOVER),
            PopAllWorkflows(),
            PushWorkflow(name=WorkflowName.GAMEOVER)
        ]
    
@dataclass
class CheckGameOverEvent(FlowEvent):
    def apply(self, ctx : ActionContext) -> list[Event]:
        print("END GAME CHECK")
        if ctx.rules.is_game_over(ctx.board, ctx.state.factions, ctx.phase):
            return [GameOverEvent()]
        return []
        
