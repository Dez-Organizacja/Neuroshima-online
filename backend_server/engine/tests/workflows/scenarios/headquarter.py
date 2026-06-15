from main.events.effects import ClearWorkflowDataEffect, DiscardTokenEffect, DrawNamedTokenEffect, PlaceEffect
from main.events.workflow import PopWorkflow, PushWorkflow, ConsumeOnClick
from main.events.flow import StartTurnEvent, EndTurnEvent
from main.input.data import ActionType, BoardAction, HandAction
from main.state.context import ActionContext
from main.workflows.data import WorkflowConfig, WorkflowName

from .builder import ScenarioBuilder
from .registry import register


@register(WorkflowName.HEADQUARTER_TURN)
def headquarter_turn_scenario():
    def setup_function(ctx: ActionContext):
        ctx.faction = ""
        ctx.state.players["moloch"].pile.add("sztab")

    def setup_hand(ctx: ActionContext):
        ctx.player.hand.add("sztab")

    def setup_factions(ctx : ActionContext):
        ctx.turn_faction = "moloch"
        ctx.faction = "moloch"

    return (
        ScenarioBuilder(
            WorkflowName.HEADQUARTER_TURN,
            config=WorkflowConfig(faction="moloch"),
        )
        .tick()
        .given(setup_function)
        .then_execution(
            events=[
                StartTurnEvent(faction="moloch"), 
                ClearWorkflowDataEffect()]
        )
        
        .tick()
        .given(setup_factions)
        .then_execution(events=[DrawNamedTokenEffect("sztab")])

        .when(HandAction(slot=0))
        .given(setup_hand)
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(type=ActionType.HAND, slot=0)

        .tick()
        .then_execution(events=[PushWorkflow(name=WorkflowName.HAND)])

        .tick()
        .then_execution(
            events=[EndTurnEvent(turn_name=WorkflowName.HEADQUARTER_TURN)]
        )
    ).build()


# @register(WorkflowName.HEADQUARTER_PLACE)
# def headquarter_place_scenario():
#     def setup_function(ctx: ActionContext):
#         ctx.workflow_data.set_slot(0)
#         ctx.player.hand.add("sztab")

#     return (
#         ScenarioBuilder(WorkflowName.HEADQUARTER_PLACE)
#         .when(BoardAction(pos=(1, 1)))
#         .given(setup_function)
#         .then_data_delta(type=ActionType.BOARD, unit_pos=(1, 1), slot=0)

#         .tick()
#         .then_execution(
#             events=[
#                 PlaceEffect(pos=(1, 1), name="sztab", faction="moloch"),
#                 DiscardTokenEffect(slot=0),
#                 PopWorkflow(),
#             ]
#         )
#     ).build()
