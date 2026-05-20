from main.state.contex import ActionContext
from main.events.base import Event
from abc import ABC

class Effect(Event, ABC):
    pass

class DiscardActiveTokenEffect(Effect):
    def __init__(self):
        pass

    def apply(self, ctx : ActionContext):
        ctx.player.hand.discard_token(ctx.workflow_data.slot)

class SwapActivePlayerEvent(Effect):
    def apply(self, ctx : ActionContext):
        ctx.state.current_fraction = ctx.rules.get_enemy(ctx, ctx.fraction)

class MoveEffect(Effect):
    def __init__(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def apply(self, ctx : ActionContext):
        ctx.board.move(self.from_pos, self.to_pos)

class PlaceEffect(Effect):
    def __init__(self, pos, unit):
        self.pos = pos
        self.unit = unit
    
    def apply(self, ctx : ActionContext):
        ctx.board.assign_to_tile(pos=self.pos, unit = self.unit)
        
class DamageProfile:
    def __init__(
        self,
        can_hit_hq=True,
        ignore_armor=False
    ):
        self.can_hit_hq = can_hit_hq
        self.ignore_armor = ignore_armor

class DamageEffect(Effect):
    def __init__(self, pos, power, profile=None):
        self.pos = pos
        self.power = power
        self.profile = profile or DamageProfile()
    
    def apply(self, ctx : ActionContext):
        ctx.board.deal_damage_effect(self.pos, self.power, self.profile)

class RotateEffect(Effect):
    def __init__(self, pos, rotation):
        super().__init__()
        self.pos = pos
        self.rotation = rotation
    
    def apply(self, ctx : ActionContext):
        ctx.board.rotate(self.pos, self.rotation)

class DestroyEffect(Effect):
    def __init__(self, pos):
        self.pos = pos
    
    def apply(self, ctx : ActionContext):
        ctx.board.destroy(self.pos)

class MarkAbilityUsedEffect(Effect):
    def apply(self, ctx):
        token = ctx.board.get_tile(ctx.workflow_data.unit_pos)
        token.ability_used = True