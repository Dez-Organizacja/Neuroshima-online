import json
from main.communication.server_message import ServerMessage
from main.main import Game
from pathlib import Path

def execute(data):
    game = Game(data.gameState)
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


def test1():
    data = wczytaj("zle2.json")
    game = execute(data)