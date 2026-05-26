from main.state.contex import ActionContext
from main.events.data import Effect
from main.workflows.data import WorkflowData
from dataclasses import dataclass
from main.tokens.abstract_token import Token

class DiscardTokenEffect(Effect):
    def __init__(self, slot):
        self.slot = slot

    def apply(self, ctx : ActionContext):
        ctx.player.hand.remove(self.slot)

class MoveEffect(Effect):
    def __init__(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def apply(self, ctx : ActionContext):
        ctx.board.move_token(self.from_pos, self.to_pos)

class PlaceEffect(Effect):
    recompute_passive = True
    def __init__(self, pos, name : str, fraction : str):
        self.pos = pos
        self.name = name
        self.fraction = fraction
    
    def apply(self, ctx : ActionContext):
        ctx.board.put_token(
            pos=self.pos, 
            name=self.name, 
            fraction=self.fraction
        )
        
@dataclass        
class DamageProfile:
    power : int = 1
    direction : int | None = None
    blockable : bool = False

class DamageEffect(Effect):
    def __init__(self, pos, profile=None):
        self.pos = pos
        self.profile = profile or DamageProfile()
    
    def apply(self, ctx : ActionContext):
        unit = ctx.board.get_token(self.pos)
        unit.take_damage(
            direction=self.profile.direction,
            damage=self.profile.power,
            blockable=self.profile.blockable
        )

class RotateEffect(Effect):
    recompute_passive = True
    def __init__(self, pos, rotation):
        super().__init__()
        self.pos = pos
        self.rotation = rotation
    
    def apply(self, ctx : ActionContext):
        ctx.board.rotate_token(self.pos, self.rotation)

class DestroyEffect(Effect):
    recompute_passive = True
    def __init__(self, pos):
        self.pos = pos
    
    def apply(self, ctx : ActionContext):
        ctx.board.destroy_token(self.pos)

class MarkAbilityUsedEffect(Effect):
    def __init__(self, pos : tuple[int, int]):
        self.pos = pos

    def apply(self, ctx : ActionContext):
        token = ctx.board.get_token(self.pos)
        token.ability_used = True

class ResetAbilityUsedEffect(Effect):
    def __init__(self, positions : list[tuple[int, int]]):
        self.positions = positions

    def apply(self, ctx : ActionContext):
        for pos in self.positions:
            token = ctx.board.get_token(pos)
            token.ability_used = False

class DrawTokensEffect(Effect):
    def __init__(self, hand_limit=3):
        self.hand_limit = hand_limit

    def apply(self, ctx : ActionContext):
        hand = ctx.player.hand
        pile = ctx.player.pile
        while hand.size < self.hand_limit and not pile.empty:
            token = pile.draw()
            hand.add(token)

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