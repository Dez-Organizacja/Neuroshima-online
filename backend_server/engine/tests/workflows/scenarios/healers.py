from main.workflows.data import WorkflowName, WorkflowConfig
from .builder import ScenarioBuilder
from .registry import register
from main.state.contex import ActionContext
from main.events.effects import HealEffect, ClearWorkflowDataEffect
from main.events.workflow import GoToStep, ConsumeOnClick
from main.input.data import ActionType, BoardAction

name = WorkflowName.HEAL
@register(name)
def heal_scenario():
    def setup_function(ctx : ActionContext):
        ctx.board.put_token(pos=(1, 3), name="klaun", faction="moloch")
        ctx.board.get_token((1, 3)).add_wounds(1)
        ctx.board.put_token(pos=(1, 1), name="medyk", faction="moloch")
        ctx.board.get_token((1, 1)).set_rotation(1)

    return (
        ScenarioBuilder(name, config=WorkflowConfig(faction="moloch"))
        .tick()
        .given(setup_function)
        .then_execution(
            events=[ClearWorkflowDataEffect()]
        )
        .then_faction("moloch")

        .tick()

        .when(BoardAction((1, 1)))
        .then_execution(events=[ConsumeOnClick()])
        .then_data_delta(unit_pos=(1, 1), type=ActionType.BOARD)

        .when(BoardAction((1, 3)))
        .given_wf_onclick_consumed()
        .then_data_delta(target_pos=(1, 3))

        .tick()
        .then_execution(
            events=[HealEffect(source_pos=(1, 1), target_pos=(1, 3))]
        )

        .tick()
        .then_execution(
            events=[GoToStep(index=0)],
            advance=False
        )
    ).build()