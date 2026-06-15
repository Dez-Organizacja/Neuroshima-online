from dataclasses import dataclass, field
from enum import Enum
from main.input.data import ActionType
from main.tokens.data import Ability, BattleAbility
from main.input.data import Button
from typing import TypeVar
from main.events.data import Event, OnClickData

Hex = tuple[int, int]
    
class WorkflowName(Enum):
    MOVE = "move"
    PUSH = "push"
    ROTATE = "rotate"
    BOMB = "bomb"
    GRENADE = "grenade"
    SNIPER = "sniper"
    BATTLE = "battle"
    TURN = "turn"
    BOARD = "board"
    HAND = "hand"
    PLACE = "place"
    START_BATTLE = "start_battle"
    GAME = "game"
    HEAL = "heal"
    HEADQUARTER_TURN = "headquarter_turn"
    HEADQUARTER_PLACE = "headquarter_place"
    INITIATIVE = "initiative"
    EXPLOSION = "explosion"
    DAMAGE_RESOLVE = "damage_resolve"
    END_TURN_CONFIRM = "end_turn_confirm"
    DRAW="draw"
    GAMEOVER="gameover"
    ENDGAMESEQUENCE="end_game_sequence"
    ACTION="action"
    END_ACTION="end_action"

ABILITY_WORKFLOW_REGISTRY = {
    Ability.MOVE : WorkflowName.MOVE,
    Ability.BOMB : WorkflowName.BOMB,
    Ability.GRENADE : WorkflowName.GRENADE,
    Ability.SNIPER : WorkflowName.SNIPER,
    Ability.PUSH : WorkflowName.PUSH,
    Ability.BATTLE : WorkflowName.START_BATTLE,
}
BATTLE_ABILITY_WORKFLOW_REGISTRY = {
    BattleAbility.EXPLOSIN : WorkflowName.EXPLOSION   
}
    
@dataclass
class WorkflowData:
    slot        : int | None = None
    unit_pos    : Hex | None = None
    target_pos  : Hex | None = None
    destination : Hex | None = None
    rotation    : int | None = None
    type        : ActionType | None = None
    button      : Button | None = None


    # @classmethod
    # def from_dict(cls, data):
    #     return from_dict_dataclass(cls, data) 
    
    # def to_dict(self):
    #     return to_dict_dataclass(self)
    
    @property
    def decision(self) -> bool:
        return self.button == Button.YES

    def set_unit_pos(self, value):
        self.unit_pos = value
    
    def set_target_pos(self, value):
        self.target_pos = value
    
    def set_destination(self, value):
        self.destination = value

    def set_slot(self, value):
        self.slot = value

    def set_type(self, value):
        self.type = value

    def set_rotation(self, value):
        self.rotation = value

    def set_button(self, value):
        self.button = value


@dataclass
class WorkflowConfig:
    faction : str = ""
    factions : list[str] = field(default_factory=list)
    on_click : OnClickData = field(default_factory=OnClickData)
    
    initiative : int | None = None
    
    pos : tuple[int, int] | None = None
    
    hand_limit : int = 3

@dataclass
class WorkflowInstance:
    name : WorkflowName
    current_step_index : int | None = None
    config : WorkflowConfig = field(default_factory=WorkflowConfig)
    on_click_consumed : bool = False

@dataclass
class UndoSnapshot:
    workflow_name : WorkflowName
    owner_faction : str
    snapshot : dict
