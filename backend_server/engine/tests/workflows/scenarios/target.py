from main.workflows.data import WorkflowName
from main.events.workflow import PopWorkflow
from main.events.effects import DestroyEffect, DamageEffect, DamageProfile
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
            effects=[DestroyEffect(pos=(2, 4))],
            workflows=[PopWorkflow()]
        )
    ).build()

name2 = WorkflowName.SNIPER
@register(name2)
def sniper_scenario():
    return (
        build_prescenario(name2)
        .tick()
        .then_execution(
            effects=[DamageEffect(pos=(2, 4))],
            workflows=[PopWorkflow()]
        )
    ).build()

name3 = WorkflowName.BOMB
@register(name3)
def bomb_scenario():
    def damage_effects() -> list[DamageEffect]:
        return [
            DamageEffect(pos=(1, 5)),
            DamageEffect(pos=(2, 2)),
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
            effects=damage_effects(),
            workflows=[PopWorkflow()]
        )
    ).build()