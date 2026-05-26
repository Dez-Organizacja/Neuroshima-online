from dataclasses import dataclass

@dataclass
class ActionMessage:
    messageType : str
    gameState : dict
    userAction : dict