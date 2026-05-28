from enum import Enum

class TokenKey(Enum):
    TYPE = "type"
    X = "x"
    Y = "y"
    NAME = "name"
    ROTATION = "rotation"
    DAMAGE = "rany"
    FACTION = "frakcja"
    WIRED = "zasieciowany"
    UNIT_COUNT = "liczbajednostek"
    ABILITY = "ability"

class TokenRelation(Enum):
    OWN = "own"
    ENEMY = "enemy"
    ALL = "all"

class TokenType(Enum):
    BOARD = "plansza"
    INSTANT = "natychmiastowy"

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

class Ability(Enum):
    BATTLE = "bitwa"
    MOVE = "ruch"
    BOMB = "bomba"
    GRENADE = "granat"
    SNIPER = "snajper"
    PUSH = "odepchniecie"
    NO_ABILITY = "none"

class Token:
    TYPE = TokenKey.TYPE
    X = TokenKey.X
    Y = TokenKey.Y
    NAME = TokenKey.NAME
    ROTATION = TokenKey.ROTATION
    DAMAGE = TokenKey.DAMAGE
    FACTION = TokenKey.FACTION
    WIRED = TokenKey.WIRED

    class Stats:
        ARMOR = TokenStats.ARMOR
        WIRE = TokenStats.WIRE
        HP = TokenStats.HP
        ATTACKS = TokenStats.ATTACKS
        BOOSTS = TokenStats.BOOSTS
        BOOST_TARGET = TokenStats.BOOST_TARGET
        INITIATIVE = TokenStats.INITIATIVE