from main.workflows.data import WorkflowName
from main.input.data import BoardAction
from main.events.effects import MoveEffect
from main.events.workflow import PopWorkflow, PushWorkflow

from workflow_tester import WorkflowTester, SetupFn
from scenario_builder import ScenarioBuilder
from main.state.contex import ActionContext

# def test_move():
#     scenario = (
#         ScenarioBuilder(WorkflowName.MOVE)
#         .when(BoardAction(pos = (1, 1)))
#         .then_data(type=BoardAction.type, unit_pos = (1, 1))

#         .when(BoardAction(pos = (1, 3)))
#         .then_data(type=BoardAction.type, destination = (1, 3))

#         .when(None)
#         .then_execution(effects=[MoveEffect(from_pos=(1, 1), to_pos=(1, 3))])
        
#         .when(None)
#         .then_execution(workflows=[PushWorkflow(WorkflowName.ROTATE)])

#         .when(None)
#         .then_execution(workflows=[PopWorkflow()])
#     ).build()

#     WorkflowTester.run()
