
# from main.workflows.data import WorkflowName, WorkflowConfig
# from main.tokens.token_factory import TokenFactory
# from .registry import register
# from .builder import ScenarioBuilder
# from main.state.contex import ActionContext
# from main.events.effects import MarkActivatedUnitsEffect
# from main.events.workflow import PushWorkflow
# from main.systems.passive_systems import PassiveSystems

# @register(WorkflowName.INITIATIVE)
# def initiative_scenario():
#     def put_token_with_rotation(
#             ctx : ActionContext,
#             pos : tuple[int, int], 
#             name : str,
#             faction : str,
#             rotation : int = 0,
#         ):
#         token = TokenFactory.create(name, faction)
#         token.set_rotation(rotation)
#         ctx.board.add_token(pos, token)

#     def setup_function(ctx : ActionContext):
#         ctx.factions = ["moloch", "borgo"]
#         put_token_with_rotation(ctx, pos=(1, 3), name="lowca", faction="moloch", rotation=1)
#         put_token_with_rotation(ctx, pos=(2, 2), name="sztab", faction="moloch")
#         put_token_with_rotation(ctx, pos=(2, 4), name="sztab", faction="borgo")
#         put_token_with_rotation(ctx, pos=(2, 6), name="zabojca", faction="borgo", rotation=5)
#         put_token_with_rotation(ctx, pos=(3, 3), name="mutek", faction="borgo")
#         put_token_with_rotation(ctx, pos=(3, 5), name="klaun", faction="moloch")
#         put_token_with_rotation(ctx, pos=(4, 4), name="zawiadowca", faction="moloch")
#         PassiveSystems.compute(ctx)

#     return (
#         ScenarioBuilder(WorkflowName.INITIATIVE, config=WorkflowConfig(initiative=3))

#         .tick()
#         .given(setup_function)
#         .then_execution(events=[
#             MarkActivatedUnitsEffect(
#                 positions=[(1, 3), (3, 3), (3, 5)], 
#                 initiative=3
#             ),
#         ])

#         .build()
#         # .tick()
#         # .then_execution()
#     )