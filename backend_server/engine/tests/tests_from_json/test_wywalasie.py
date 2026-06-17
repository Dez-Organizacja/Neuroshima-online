import json
from main.communication.server_message import ServerMessage
# from main.communication.komunikacja import 
from main.main import Game
from pathlib import Path

def execute(data : ServerMessage):
    game = Game()
    game.load(data.gameState)
    # print(f"pending attacks")
    # print(game.state.pending_attacks)
    game.handle_action(data.userAction)
    return game

def wczytaj(name):
    current_dir = Path(__file__).parent
    path = current_dir / name
    with open(path, "r") as file:
        data = file.read()
    data = json.loads(data)
    
    # print(type(data))
    return ServerMessage(**data)


# def test1():
#     data = wczytaj("zle2.json")
#     game = execute(data)
#     # for instance in game.state.workflow_stack:
#     #     print(instance.name)
#     # token = game.state.board.get_token((1, 7))
#     # print(token)
#     # print(game.export())
#     print(game.animations)
#     # v = game.build_user_view()
#     # print(v["availableActions"]["board"])
#     assert False