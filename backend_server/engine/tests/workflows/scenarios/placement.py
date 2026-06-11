from main.workflows.data import WorkflowName
from main.input.data import BoardAction
from main.events.effects import ClearSelectedHandSlotEffect, DiscardTokenEffect, PlaceEffect
from main.events.workflow import PopWorkflow, PushWorkflow, ConsumeOnClick
from main.state.contex import ActionContext

from .builder import ScenarioBuilder
from .registry import register


name = WorkflowName.PLACE
@register(name)
def placement_scenario():
    def setup_function(ctx : ActionContext):
        print(f"setup ctx {ctx}")
        ctx.workflow_data.set_slot(0)
        ctx.faction = "moloch"
        ctx.player.hand.add("klaun")

    return (
        ScenarioBuilder(name)
        
        .when(BoardAction(pos = (1, 1)))
        .given(setup_function)
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(type=BoardAction.type, unit_pos=(1, 1), slot=0)

        .tick()
        .then_execution(
            events = [
                PlaceEffect(pos=(1, 1), name="klaun", faction="moloch"),
                DiscardTokenEffect(slot=0),
                ClearSelectedHandSlotEffect(),
                PushWorkflow(name=WorkflowName.ROTATE)
            ]
        )
        
        .tick()
        .then_execution(events=[PopWorkflow()])
    ).build()
