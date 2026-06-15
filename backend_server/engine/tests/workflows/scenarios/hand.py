from .builder import ScenarioBuilder
from main.workflows.data import WorkflowName, WorkflowConfig
from main.events.data import OnClickData
from main.events.workflow import PopWorkflow, PushWorkflow
from main.events.effects import DiscardTokenEffect
from main.input.data import ActionType
from .registry import register
from main.state.context import ActionContext

name = WorkflowName.HAND
@register(name)
def hand_scenario():
    def setup_function(ctx : ActionContext):
        ctx.faction = "moloch"
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
            events=[PopWorkflow()]
        )
    ).build()

@register(name)
def hand_board_token_with_ability_scenario():
    def setup_function(ctx : ActionContext):
        ctx.faction = "posterunek"
        ctx.player.hand.add("biegacz")
        ctx.workflow_data.slot = 0

    return (
        ScenarioBuilder(name, factions=["posterunek", "moloch"])
        .tick()
        .given(setup_function)
        .then_execution(
            events=[PushWorkflow(WorkflowName.PLACE)]
        )

        .tick()
        .then_execution(
            events=[PopWorkflow()]
        )
    ).build()

@register(name)
def hand_instant_token_with_ability_scenario():
    def setup_function(ctx : ActionContext):
        ctx.faction = "posterunek"
        ctx.player.hand.add("ruch")
        ctx.workflow_data.slot = 0

    return (
        ScenarioBuilder(name, factions=["posterunek", "moloch"])
        .tick()
        .given(setup_function)
        .then_execution(
            events=[
                PushWorkflow(
                    name=WorkflowName.MOVE, 
                    config=WorkflowConfig(on_click=OnClickData(discard_slot=0))
                )
            ]
        )

        .tick()
        .then_execution(
            events=[PopWorkflow()]
        )
    ).build()
