from dataclasses import dataclass
from typing import ClassVar
from main.events.data import FlowEvent, Effect, Event
from main.events.workflow import PushWorkflow, PopWorkflow, DeleteAbove
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName
from main.attacks.resolver import AttackResolver

@dataclass
class EndTurnEvent(FlowEvent):
    def apply(self, ctx: ActionContext) -> list[Event]:
        return [
            DeleteAbove(name=WorkflowName.TURN),
            PopWorkflow(),
        ]

# @dataclass
# class StartBattleEvent(FlowEvent):
#     def apply(self, ctx: ActionContext) -> list[Event]:
#         return [
#             flow_events=[EndTurnEvent()],
#             workflow_effects=[PushWorkflow(WorkflowName.BATTLE)],
#         ]
