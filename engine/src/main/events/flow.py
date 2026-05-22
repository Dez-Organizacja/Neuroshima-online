from abc import ABC
from main.events.data import Event, ExecutionResult, ActionResult
from main.events.workflow import PushWorkflow, PopWorkflow
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName
from main.workflows.turn import TurnWorkflow

class FlowEvent(ABC, Event):
    pass

class EndTurnEvent(FlowEvent):
    def apply(self, ctx : ActionContext) -> ExecutionResult:
        ExecutionResult(
            action_result=TurnWorkflow.end_turn_resolve(ctx),
            workflow_effects=[PopWorkflow()]
        )

class StartBattleEvent(FlowEvent):
    def apply(self, ctx : ActionContext) -> ExecutionResult:
        ExecutionResult(
            action_result=ActionResult(flow_events=[EndTurnEvent()]),
            workflow_effects=[PushWorkflow(WorkflowName.BATTLE)],
        )