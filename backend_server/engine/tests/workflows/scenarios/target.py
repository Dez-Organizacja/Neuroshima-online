from main.workflows.data import WorkflowName
from main.events.workflow import PopWorkflow
from main.events.effects import DestroyEffect, EnqueueAttacksEffect
from main.events.data import TargetedAttackIntent
from main.events.flow import ResolveAttacksEvent
from .builder import ScenarioBuilder
from .registry import register
from main.input.data import BoardAction, ActionType
from main.state.contex import ActionContext

def build_prescenario(name : WorkflowName) -> ScenarioBuilder:
    return (
        ScenarioBuilder(name)
        .when(BoardAction(pos=(2, 4)))
        .then_data_delta(target_pos=(2, 4), type=ActionType.BOARD)
    )

name1 = WorkflowName.GRENADE
@register(name1)
def granade_scenario():
    return (
        build_prescenario(name1)
        .tick()
        .then_execution(
            events=[
                DestroyEffect(pos=(2, 4)),
                PopWorkflow()
            ]
        )
    ).build()

name2 = WorkflowName.SNIPER
@register(name2)
def sniper_scenario():
    return (
        build_prescenario(name2)
        .tick()
        .then_execution(
            events=[
                EnqueueAttacksEffect(
                    [TargetedAttackIntent(target_pos=(2, 4))]
                ),
                ResolveAttacksEvent(),
                PopWorkflow()
            ]
        )
    ).build()

name3 = WorkflowName.BOMB
@register(name3)
def bomb_scenario():
    def damage_effects() -> list[TargetedAttackIntent]:
        return [
            TargetedAttackIntent(target_pos=(1, 5)),
            TargetedAttackIntent(target_pos=(2, 2)),
        ]
    def setup_function(ctx : ActionContext):
        ctx.board.put_token(pos=(2, 6), name="sztab", faction="moloch")
        ctx.board.put_token(pos=(2, 2), name="klaun", faction="moloch")
        ctx.board.put_token(pos=(1, 5), name="sieciarz", faction="borgo")

    return (
        ScenarioBuilder(name3)
        .when(BoardAction(pos=(2, 4)))
        .given(setup_function)
        .then_data_delta(target_pos=(2, 4), type=ActionType.BOARD)
        .tick()
        .then_execution(
            events=[
                EnqueueAttacksEffect(damage_effects()),
                ResolveAttacksEvent(),
                PopWorkflow(),
            ]
        )
    ).build()