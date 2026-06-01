from dataclasses import dataclass, field

@dataclass
class ServerMessage:
    messageType : str
    timestamp : str
    gameState : dict
    userAction : dict = field(default_factory=dict)