from main.view.builder import GameViewBuilder
from main.engine.engine import GameEngine
from main.engine.resolver import Resolver
from main.state.context import ActionContext
from main.state.game_state import GameState
from main.rules.game import GameRules
from main.main import Game
from main.communication.server_message import ServerMessage
from main.state.serialization import Serializator
import json

class Tests:
    def test_view(self):
        game = Game()
        game.start_game({"factions" : ["moloch", "borgo"]})
        post = ServerMessage(
            messageType="GAMEVIEW_REQUEST",
            timestamp="2026-06-11T23:13:59.107120696",
            gameState=game.export(),
        )
        data = Serializator.to_dict_dataclass(post)
        json_string = json.dumps(data)
        print(json_string)
        data_dict = json.loads(json_string)
        message = ServerMessage(**data_dict)
        game = Game()
        game.load(message.gameState)
        game.build_user_view()
        # assert False