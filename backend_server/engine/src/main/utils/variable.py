from enum import Enum

class Phase(Enum):
    START_GAME = "newgame"
    GAME = "game"
    ENDGAME="endgame"
    GAMEOVER="gameover"

class Relation(Enum):
    EMPTY = "empty"
    OWN = "own"
    ENEMY = "enemy"
