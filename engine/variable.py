class State:
    NO_SELECTION = "no_selection"
    SELECTED_HAND = "selected_hand"
    SELECTED_BOARD = "selected_hand"
    ROTATE = "rotate"

class Bottom:
    END_TURN = "end_turn"
    DISCARD = "discard"
    USE = "use"
    CANCEL = "cancel"
    YES = "yes"
    NO = "no"

class Action_Type:
    BOARD = "board"
    HAND = "hand"
    ROTATE = "rotate"
    BOTTOM = "bottom"

class Instant_Token:
    BITWA = "bitwa"

class Variable:
    AVAILABLE_ACTIONS = "available_actions"
    USE = "use"
    RUN = "run"
    BITWA = "bitwa"
    ALL = "all"

class Token_Type:
    ON_BOARD = "plansza"
    INSTANT = "natychmiastowy"

class Turn_Type:
    LAST = "ostatnia"
    STANDARD = "tura"
    HQ_PLACEMENT = "wystaw_sztab"