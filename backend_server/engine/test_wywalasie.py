import json
from main.communication.server_message import ServerMessage
from main.main import Game

def execute(data):
    game = Game(data.gameState)
    game.handle_action(data.userAction)
    return game

def wczytaj(name):
    with open(name, "r") as file:
        data = file.read()
    data = json.loads(data)
    
    # print(type(data))
    return ServerMessage(**data)


def test2():
    data = wczytaj("zle2.json")
    game = execute(data)

