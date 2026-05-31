import json
from main.communication.action_message import ActionMessage
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
    return ActionMessage(**data)


def test2():
    data = wczytaj("zle2.json")
    game = execute(data)

