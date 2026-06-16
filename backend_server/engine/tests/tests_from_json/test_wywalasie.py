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
#     # game.handle_action({
#     #     "type" : "button",
#     #     "name" : "end_turn",
#     # })
#     # game.handle_action({
#     #     "type" : "button",
#     #     "name" : "yes",
#     # })
#     # token = game.state.board.get_token((2, 6))
#     # print(token)
#     # print(game.export())
#     # v = game.build_user_view()
#     # print(v["availableActions"])
#     assert False