from dataclasses import dataclass
from typing import ClassVar
from main.events.data import FlowEvent, Effect, Event
from main.events.workflow import PushWorkflow, PopWorkflow, DeleteAbove
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName, WorkflowConfig
from main.attacks.resolver import AttackResolver

@dataclass
class EndTurnEvent(FlowEvent):
    next_workflow : PushWorkflow | None = None
    def apply(self, ctx: ActionContext) -> list[Event]:
        effects = [
            DeleteAbove(name=WorkflowName.TURN),
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
