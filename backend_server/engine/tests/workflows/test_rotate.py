from main.workflows.data import WorkflowName
from main.input.data import RotationAction
from main.events.effects import RotateEffect
from main.events.workflow import PopWorkflow

from workflow_tester import WokrflowTester
from scenario_builder import ScenarioBuilder

def test_rotate():
    scenario = (
        ScenarioBuilder(WorkflowName.ROTATE)
        .when(RotationAction(1))
        .given(lambda d : d.set_unit_pos((1, 1)))
        .then_data(unit_pos=(1, 1), rotation=1)
        
        .when(None)
        .then_execution(
            effects=[RotateEffect(pos=(1, 1), rotation=1)],
            workflows=[PopWorkflow()]
        )
    ).build()
    WokrflowTester().run(scenario)

# def test_rotate():
#     ctx = build_contex(
#         name=WorkflowName.ROTATE,
#         data=WorkflowData(unit_pos=(1, 1))
#     )
#     wf = RotateWorkflow()
#     wf.build_steps()
#     result = execute_step(ctx, action=RotationAction(1))

#     assert result.advance
#     assert ctx.workflow_data.rotation == 1
#     assert ctx.workflow_data.unit_pos == (1, 1)

#     ctx.workflow_instance.current_step_index += 1
#     result = execute_step(ctx)

#     assert result.advance
#     effects = result.execution_result.effects
#     assert  len(effects) == 1
#     assert isinstance(effects[0], RotateEffect)
#     assert effects[0].rotation == 1
    
#     assert len(result.execution_result.flow_events) == 0

#     workflow = result.execution_result.workflow_effects
#     assert len(workflow) == 1
#     assert isinstance(workflow[0], PopWorkflow)