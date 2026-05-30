# from .builder import ScenarioBuilder
# from .registry import register
# from main.workflows.data import WorkflowName
# from main.input.data import BoardAction
# from main.state.contex import ActionContext
# from main.events.workflow import PushWorkflow, PopWorkflow
# from main.events.effects import MarkAbilityUsedEffect

# name = WorkflowName.BOARD
# @register(name)
# def board_scenario():
#     def setup_function(ctx : ActionContext):
#         ctx.workflow_data.unit_pos = (1, 1)
#         ctx.board.put_token(pos=(1, 1), name="biegacz", faction="posterunek")

#     return (
#         ScenarioBuilder(name)
#         .tick()
#         .given(setup_function)
#         .then_execution(
#             workflows=[PushWorkflow(name=WorkflowName.MOVE)]
#         )

#         .tick()
#         .then_execution(
#             effects=[MarkAbilityUsedEffect(pos=(1, 1))],
#             workflows=[PopWorkflow()]
#         )
#     ).build()