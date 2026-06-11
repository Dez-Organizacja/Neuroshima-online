from main.input.data import BoardAction, ActionType
from main.workflows.data import WorkflowName
from main.events.effects import MoveEffect
from main.events.workflow import PopWorkflow, ConsumeOnClick

from .builder import ScenarioBuilder
from .registry import register

name = WorkflowName.PUSH
@register(name)
def push_scenario():
    return (
        ScenarioBuilder(name)
        
        .when(BoardAction(pos = (1, 1)))
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(type=ActionType.BOARD, unit_pos=(1, 1))

        .when(BoardAction(pos=(1, 3)))
        .given_wf_onclick_consumed()
        .then_data_delta(target_pos=(1, 3))

        .when(BoardAction(pos=(1, 5)))
        .then_data_delta(destination=(1, 5))

        .tick()
        .then_execution(
            events=[
                MoveEffect(from_pos=(1, 3), to_pos=(1, 5)),
                PopWorkflow()
            ]
        )
    ).build()