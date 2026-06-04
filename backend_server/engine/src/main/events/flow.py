from dataclasses import dataclass
from main.events.data import FlowEvent, Event
from main.events.workflow import PushWorkflow, PopWorkflow, DeleteAbove
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName


@dataclass
class EndTurnEvent(FlowEvent):
    def apply(self, ctx: ActionContext) -> list[Event]:
        return [
            DeleteAbove(name=WorkflowName.TURN),
            PopWorkflow(),
        ]

@dataclass
class ResolveAttacksEvent:
    def apply(ctx : ActionContext):
        pass
        # while ctx.state.pending_attacks:
        #     attack = ctx.state.pending_attacks.pop()


# @dataclass
# class StartBattleEvent(FlowEvent):
#     def apply(self, ctx: ActionContext) -> list[Event]:
#         return [
#             flow_events=[EndTurnEvent()],
#             workflow_effects=[PushWorkflow(WorkflowName.BATTLE)],
#         ]