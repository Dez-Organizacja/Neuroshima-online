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

class TokenKey(Enum):
    TYPE = "type"
    X = "x"
    Y = "y"
    NAME = "name"
    ROTATION = "rotation"
    DAMAGE = "rany"
    FRACTION = "frakcja"
    WIRED = "zasieciowany"
    UNIT_COUNT = "liczbajednostek"

class TokenType(Enum):
    BOARD = "plansza"
    INSTANT = "natychmiastowy"
        
class InstantType(Enum):
            BITWA = "bitwa"
            MOVE = "ruch"
            BOMB = "bomba"
            GRENADE = "granat"
            SNIPER = "snajper"
            PUSH = "odepchniecie"

class BoardType(Enum):
    HQ = "sztab"

class TokenStats(Enum):
    ARMOR = "pancerz"
    WIRE = "siec"
    HP = "hp"
    ATTACKS = "ataki"
    BOOSTS = "modul"
    BOOST_TARGET = "boost_target"
    INITIATIVE = "inicjatywa"


class Token:
    TYPE = TokenKey.TYPE
    X = TokenKey.X
    Y = TokenKey.Y
    NAME = TokenKey.NAME
    ROTATION = TokenKey.ROTATION
    DAMAGE = TokenKey.DAMAGE
    FRACTION = TokenKey.FRACTION
    WIRED = TokenKey.WIRED

    class Stats:
        ARMOR = TokenStats.ARMOR
        WIRE = TokenStats.WIRE
        HP = TokenStats.HP
        ATTACKS = TokenStats.ATTACKS
        BOOSTS = TokenStats.BOOSTS
        BOOST_TARGET = TokenStats.BOOST_TARGET
        INITIATIVE = TokenStats.INITIATIVE



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
    FRACTION = "frakcja"

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

class Bottom(Enum):
    END_TURN = "end_turn"
    DISCARD = "discard"
    USE = "use"
    CANCEL = "cancel"
    YES = "yes"
    NO = "no"