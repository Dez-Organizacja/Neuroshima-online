from enum import Enum

class State(Enum):
    NO_SELECTION = "no_selection"
    SELECTED_HAND = "selected_hand"
    PLACING = "placing"
    ROTATE = "rotate"
    MOVING = "moving"
    SELECTED_PUSHER = "selected_pusher"
    PUSHING = "pushing"

class Selected(Enum):
    SLOT = "slot"
    POS = "pos"
    X = "x"
    Y = "y"
    PUSHER_X = "pusher_x"
    PUSHER_Y = "pusher_y"
    PUSHER_POS = "pusher_pos"
    NAME = "name"

class Attack(Enum):
    MELEE = "melee"
    SHOOT = "shoot"
    GAUSS = "gauss"

class Boost(Enum):
    MELEE = "melee"
    SHOOT = "shoot"
    INITIATIVE = "initiative"
    NEW_INITIATIVE = "new_initiative"
    HEAL = "heal"
    STEAL_BOOST = "steal_boost"



class Variable(Enum):
    ALL = "all"

# class Token_Type:
    

class Phase(Enum):
    HQ_PLACEMENT = "sztaby"
    GAME = "game"
    START_GAME = "newgame"

class Turn:
    BITWA = "bitwa"
    TYPE = "type"
    FACTION = "frakcja"

    class Type(Enum):
        LAST = "ostatnia"
        FIRST = "pierwsza"
        SECOND = "druga"
        STANDARD = "tura"
        HQ_PLACEMENT = "wystaw_sztab"

class Mode(Enum):
    AVAILABLE_ACTIONS = "available_actions"
    USE = "use"
    RUN = "run"
    VALIDATE = "validate"

class Relation(Enum):
    EMPTY = "empty"
    FRIENDLY = "friendly"
    ENEMY = "enemy"
