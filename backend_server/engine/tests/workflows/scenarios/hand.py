from .builder import ScenarioBuilder
from main.workflows.data import WorkflowName
from main.events.workflow import PopWorkflow, PushWorkflow
from main.events.effects import DiscardTokenEffect
from .registry import register
from main.state.contex import ActionContext

name = WorkflowName.HAND
@register(name)
def hand_scenario():
    def setup_function(ctx : ActionContext):
        ctx.player.hand.add("klaun")
        ctx.player.hand.add("sieciarz")
        ctx.workflow_data.slot = 1

    return (
        ScenarioBuilder(name)
        .tick()
        .given(setup_function)
        .then_execution(
            events=[PushWorkflow(WorkflowName.PLACE)]
        )

        .tick()
        .then_execution(
            events=[
                DiscardTokenEffect(slot=1),
                PopWorkflow()
            ]
        )
    ).build()