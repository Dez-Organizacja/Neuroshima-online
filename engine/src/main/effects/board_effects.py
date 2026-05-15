from main.utils.variable import State
from main.state.contex import ActionContext
from abc import ABC, abstractmethod

class BoardEffect(ABC):
    @abstractmethod
    def apply(ctx : ActionContext):
        pass

class MoveEffect():
    def __init__(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def apply(self, ctx : ActionContext):
        ctx.board.move(self.from_pos, self.to_pos)

class PlaceEffect():
    def __init__(self, pos, unit):
        self.pos = pos
        self.unit = unit
    
    def apply(self, ctx : ActionContext):
        ctx.board.assign_to_tile(pos=self.pos, unit = self.unit)


class DiscardActiveTokenEffect():
    def __init__(self):
        pass

    def apply(self, ctx : ActionContext):
        ctx.player.hand.discard_active_token()
        
class DamageProfile:
    def __init__(
        self,
        can_hit_hq=True,
        ignore_armor=False
    ):
        self.can_hit_hq = can_hit_hq
        self.ignore_armor = ignore_armor

class DamageEffect():
    def __init__(self, pos, power, profile=None):
        self.pos = pos
        self.power = power
        self.profile = profile or DamageProfile()
    
    def apply(self, ctx : ActionContext):
        ctx.board.deal_damage_effect(self.pos, self.power, self.profile)

class RotateEffect():
    def __init__(self, pos, rotation):
        self.pos = pos
        self.rotation = rotation
    
    def apply(self, ctx : ActionContext):
        ctx.board.rotate(self.pos, self.rotation)

class DestroyEffect():
    def __init__(self, pos):
        self.pos = pos
    
    def apply(self, ctx : ActionContext):
        ctx.board.destroy(self.pos)