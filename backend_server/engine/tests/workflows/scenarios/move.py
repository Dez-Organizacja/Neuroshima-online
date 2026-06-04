from main.workflows.data import WorkflowName
from main.input.data import BoardAction
from main.events.effects import MoveEffect
from main.events.workflow import PopWorkflow, PushWorkflow

from .registry import register
from .builder import ScenarioBuilder

name = WorkflowName.MOVE
@register(name)
def move_scenario():
    return (
        ScenarioBuilder(name)
        .when(BoardAction(pos = (1, 1)))
        .then_data_delta(type=BoardAction.type, unit_pos = (1, 1))

        .when(BoardAction(pos = (1, 3)))
        .then_data_delta(destination = (1, 3))

        .tick()
        .then_execution(events=[MoveEffect(from_pos=(1, 1), to_pos=(1, 3))])
        
        # .tick()
        # .then_execution(workflows=[PushWorkflow(WorkflowName.ROTATE)])  

        .tick()
        .then_execution(events=[PopWorkflow()])
    ).build()