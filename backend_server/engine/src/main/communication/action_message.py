from dataclasses import dataclass

@dataclass
class ActionMessage:
    messageType : str
    timestamp : str
    gameState : dict
    userAction : dict