from main.workflows.data import WorkflowName, WorkflowConfig
from main.events.workflow import PopWorkflow, PushWorkflow, ConsumeOnClick
from main.events.effects import DestroyEffect, EnqueueAttacksEffect
from main.attacks.data import TargetedIntent
from .builder import ScenarioBuilder
from .registry import register
from main.input.data import BoardAction, ActionType
from main.state.context import ActionContext

def build_prescenario(name : WorkflowName) -> ScenarioBuilder:
    return (
        ScenarioBuilder(name)
        .when(BoardAction(pos=(2, 4)))
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(target_pos=(2, 4), type=ActionType.BOARD)
    )

name1 = WorkflowName.GRENADE
@register(name1)
def granade_scenario():
    return (
        build_prescenario(name1)
        .tick()
        .then_execution(events=[DestroyEffect(pos=(2, 4))])

        .tick()
        .then_execution(events=[PopWorkflow()])
        
    ).build()

name2 = WorkflowName.SNIPER
factions=["moloch", "borgo"]
@register(name2)
def sniper_scenario():
    return (
        build_prescenario(name2)
        .tick()
        .then_execution(
            events=[
                EnqueueAttacksEffect(
                    [TargetedIntent(target_pos=(2, 4))]
                ),
                PushWorkflow(
                    name=WorkflowName.DAMAGE_RESOLVE,
                    config=WorkflowConfig(factions=factions)
                ),
            ]
        )

        .tick()
        .then_execution(events=[PopWorkflow()])
    
    ).build()

name3 = WorkflowName.BOMB
@register(name3)
def bomb_scenario():
    def damage_effects() -> list[TargetedIntent]:
        return [
            TargetedIntent(target_pos=(1, 5)),
            TargetedIntent(target_pos=(2, 2)),
        ]
    def setup_function(ctx : ActionContext):
        ctx.board.put_token(pos=(2, 6), name="sztab", faction="moloch")
        ctx.board.put_token(pos=(2, 2), name="klaun", faction="moloch")
        ctx.board.put_token(pos=(1, 5), name="sieciarz", faction="borgo")

    return (
        ScenarioBuilder(name3)
        .when(BoardAction(pos=(2, 4)))
        .given(setup_function)
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(target_pos=(2, 4), type=ActionType.BOARD)
        
        .tick()
        .given_wf_onclick_consumed()
        .then_execution(
            events=[
                EnqueueAttacksEffect(damage_effects()),
                PushWorkflow(
                    name=WorkflowName.DAMAGE_RESOLVE,
                    config=WorkflowConfig(factions=factions)
                ),
            ]
        )

        .tick()
        .then_execution(events=[PopWorkflow()])
    
    ).build()