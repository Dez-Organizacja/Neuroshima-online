from main.workflows.data import WorkflowName
from main.input.data import RotationAction
from main.events.effects import RotateEffect
from main.events.workflow import PopWorkflow, ConsumeOnClick

from .builder import ScenarioBuilder
from .registry import register

name = WorkflowName.ROTATE
@register(name)
def rotate_scenario():
    return (
        ScenarioBuilder(name)
        .when(RotationAction(1))
        .given(lambda d : d.workflow_data.set_unit_pos((1, 1)))
        # .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(type=RotationAction.type, unit_pos=(1, 1), rotation=1)
        
        .tick()
        # .given_wf_onclick_consumed()
        .then_execution(
            events=[RotateEffect(pos=(1, 1), rotation=1)]
        )

        .tick()
        .then_execution(events=[PopWorkflow()])
    ).build()