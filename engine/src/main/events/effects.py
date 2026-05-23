from main.state.contex import ActionContext
from main.events.data import Effect
from main.workflows.data import WorkflowData

class DiscardActiveTokenEffect(Effect):
    def __init__(self):
        pass

    def apply(self, ctx : ActionContext):
        ctx.player.hand.discard_token(ctx.workflow_data.slot)

class MoveEffect(Effect):
    def __init__(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def apply(self, ctx : ActionContext):
        ctx.board.move(self.from_pos, self.to_pos)

class PlaceEffect(Effect):
    recompute_passive = True
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
    recompute_passive = True
    def __init__(self, pos, rotation):
        super().__init__()
        self.pos = pos
        self.rotation = rotation
    
    def apply(self, ctx : ActionContext):
        ctx.board.rotate(self.pos, self.rotation)

class DestroyEffect(Effect):
    recompute_passive = True
    def __init__(self, pos):
        self.pos = pos
    
    def apply(self, ctx : ActionContext):
        ctx.board.destroy(self.pos)

class MarkAbilityUsedEffect(Effect):
    def apply(self, ctx):
        token = ctx.board.get_tile(ctx.workflow_data.unit_pos)
        token.ability_used = True

class ResetAbilityUsedEffect(Effect):
    def __init__(self, positions : list[tuple[int, int]]):
        self.positions = positions

    def apply(self, ctx : ActionContext):
        for pos in self.positions:
            token = ctx.board.get_tile(pos)
            token.ability_used = False

class DrawTokensEffect(Effect):
    def __init__(self, hand_limit=3):
        self.hand_limit = hand_limit

    def apply(self, ctx : ActionContext):
        hand = ctx.player.hand
        pile = ctx.player.pile
        while hand.size < self.hand_limit and not pile.empty:
            token = pile.get_token()
            hand.draw_token(token)

class ClearWorkflowDataEffect(Effect):
    def apply(self, ctx):
        ctx.workflow_data = WorkflowData()

class RemoveDeadUnitsEffect(Effect):
    recompute_passive = True
    def __init__(self, positions : list[tuple[int, int]]):
        self.positions = positions

    def apply(self, ctx : ActionContext):
        for pos in self.positions:
            ctx.board.remove_token(pos)