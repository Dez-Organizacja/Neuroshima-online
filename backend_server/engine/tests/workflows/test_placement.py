from main.workflows.data import WorkflowName
from main.input.data import BoardAction
from main.events.effects import PlaceEffect
from main.events.workflow import PopWorkflow

from workflow_tester import WorkflowTester, SetupFn
from scenario_builder import ScenarioBuilder
from main.state.contex import ActionContext


def test_placement():
    def setup_function(ctx : ActionContext):
        print(f"setup ctx {ctx}")
        ctx.workflow_data.set_slot(0)
        ctx.player.hand.add("klaun")

    scenario = (
        ScenarioBuilder(WorkflowName.PLACE)
        
        .when(BoardAction(pos = (1, 1)))
        .given(setup_function)
        .then_data(type=BoardAction.type, unit_pos=(1, 1), slot=0)

        .when(None)
        .then_execution(
            effects = [PlaceEffect(pos=(1, 1), name="klaun", faction="moloch")],
            workflows=[PopWorkflow()]
        )
    ).build()

    WorkflowTester().run(scenario)
