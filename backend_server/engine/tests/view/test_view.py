# from main.view.builder import GameViewBuilder
# from main.engine.engine import GameEngine
# from main.engine.resolver import Resolver
# from main.state.contex import ActionContext
# from main.state.game_state import GameState
# from main.rules.game import GameRules
# import json

# class Tests:
#     def test_view(self):
#         engine = GameEngine(resolver=Resolver())
#         builder = GameViewBuilder()
#         ctx = ActionContext(
#             state=GameState(fractions=["moloch", "borgo"]), 
#             rules=GameRules()
#         )
#         engine.start_game(ctx)
#         view = builder.build(ctx)
#         json_string = json.dumps(view)

#         print(json_string)
#         assert False