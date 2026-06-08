from enum import Enum
from dataclasses import dataclass

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
    ABILITIES = "abilities"

class AbilityType(Enum):
    ABILITY = "ability"
    BATTLE_ABILITY = "battle_ability"

class BattleAbility(Enum):
    EXPLOSIN = "explosion"
    NO_ABILITY = "none"

class Ability(Enum):
    BATTLE = "bitwa"
    MOVE = "ruch"
    BOMB = "bomba"
    GRENADE = "granat"
    SNIPER = "snajper"
    PUSH = "odepchniecie"
    NO_ABILITY = "none"

class Boost(Enum):
    MELEE = "melee"
    SHOOT = "shoot"
    INITIATIVE = "initiative"
    MINUS_INITIATIVE = "minus_initiative"
    SET_INITIATIVE_TO_0 = "set_initiative_to_0"
    NEW_INITIATIVE = "new_initiative"
    MEELE_TO_SHOOT = "meele_to_shoot"
    MOVE_ABILITY = "move_ability"
    HEAL = "heal"
    STEAL_BOOST = "steal_boost"

@dataclass
class TokenView:
    faction : str
    name : str
    rotation : int
    wired : bool
    ability_used : bool
    damage : int