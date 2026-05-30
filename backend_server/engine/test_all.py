from main.main import Game
from main.communication.action_message import ActionMessage
import json

def test_all():
    with open("data.json", "r") as file:
        data = file.read()

    data = json.loads(data)
    
    # print(type(data))
    data = ActionMessage(**data)
    # print(data)
    game = Game(data.gameState)
    game.handle_action(data.userAction)
    print(game.build_user_view())
    # print(game)
    # assert False