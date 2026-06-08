from enum import Enum

class Phase(Enum):
    HQ_PLACEMENT = "sztaby"
    GAME = "game"
    START_GAME = "newgame"

class Relation(Enum):
    EMPTY = "empty"
    OWN = "own"
    ENEMY = "enemy"
