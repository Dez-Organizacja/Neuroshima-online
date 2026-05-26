from dataclasses import dataclass
from main.events.data import ExecutionResult, FlowEvent
from main.events.workflow import PushWorkflow, PopWorkflow, DeleteAbove
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName


@dataclass
class EndTurnEvent(FlowEvent):
    def apply(self, ctx: ActionContext) -> ExecutionResult:
        return ExecutionResult(
            workflow_effects=[
                DeleteAbove(name=WorkflowName.TURN),
                PopWorkflow(),
            ]
        )


@dataclass
class StartBattleEvent(FlowEvent):
    def apply(self, ctx: ActionContext) -> ExecutionResult:
        return ExecutionResult(
            flow_events=[EndTurnEvent()],
            workflow_effects=[PushWorkflow(WorkflowName.BATTLE)],
        )