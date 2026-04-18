class State:
    NO_SELECTION = "no_selection"
    SELECTED_HAND = "selected_hand"
    PLACING = "placing"
    ROTATE = "rotate"
    MOVING = "moving"
    SELECTED_PUSHER = "selected_pusher"
    PUSHING = "pushing"

class UI:
    BOTTOM = "bottom"
    HAND = "hand"
    BOARD = "board"

class Selected:
    SLOT = "slot"
    X = "x"
    Y = "y"
    PUSHER_X = "pusher_x"
    PUSHER_Y = "pusher_y"
    NAME = "name"


class Attack:
    MELEE = "melee"
    SHOOT = "shoot"
    GAUSS = "gauss"

class Token:
    TYPE = "type"
    X = "x"
    Y = "y"
    NAME = "name"
    ROTATION = "rotation"
    DAMAGE = "rany"
    FRACTION = "frakcja"
    WIRED = "zasieciowany"
    UNIT_COUNT = "liczbajednostek"
    class Type:
        BOARD = "plansza"
        INSTANT = "natychmiastowy"
        class Instant:
            BITWA = "bitwa"
            MOVE = "ruch"
            BOMB = "bomba"
            GRENADE = "granat"
            SNIPER = "snajper"
            PUSH = "odepchniecie"
        class Board:
            HQ = "sztab"

    class Stats:
        ARMOR = "pancerz"
        WIRE = "siec"
        HP = "hp"
        ATTACKS = "ataki"
        INITIATIVE = "inicjatywa"


class Bottom:
    END_TURN = "end_turn"
    DISCARD = "discard"
    USE = "use"
    CANCEL = "cancel"
    YES = "yes"
    NO = "no"

class Action:

    class Key:
        TYPE = "type"
        X = "x"
        Y = "y"
        SLOT = "slot"
        BOTTOM = "bottom"
        ROTATION = "rotation"

    class Type:
        BOARD = "board"
        HAND = "hand"
        ROTATE = "rotate"
        BOTTOM = "bottom"

class Variable:
    ALL = "all"

# class Token_Type:
    

class Phase:
    HQ_PLACEMENT = "sztaby"
    GAME = "game"
    START_GAME = "newgame"

class Turn:
    BITWA = "bitwa"
    TYPE = "type"
    FRACTION = "frakcja"
    class Type:
        LAST = "ostatnia"
        FIRST = "pierwsza"
        SECOND = "druga"
        STANDARD = "tura"
        HQ_PLACEMENT = "wystaw_sztab"

class Mode:
    AVAILABLE_ACTIONS = "available_actions"
    USE = "use"
    RUN = "run"
    VALIDATE = "validate"
