from dataclasses import dataclass, field
from typing import ClassVar
from main.state.contex import ActionContext
from main.events.data import Effect
from main.attacks.data import AttackIntent
from main.workflows.data import WorkflowData

# ----------- moving and placing -----------

@dataclass
class MoveEffect(Effect):
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        ctx.board.move_token(self.from_pos, self.to_pos)
        ctx.workflow_data.set_unit_pos(ctx.workflow_data.destination)

@dataclass
class RotateEffect(Effect):
    pos: tuple[int, int]
    rotation: int
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        ctx.board.get_token(self.pos).set_rotation(self.rotation)

@dataclass
class PlaceEffect(Effect):
    pos: tuple[int, int]
    name: str
    faction: str
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        ctx.board.put_token(
            pos=self.pos,
            name=self.name,
            faction=self.faction,
        )

@dataclass
class EnqueueAttacksEffect(Effect):
    attack : list[AttackIntent]

    def apply(self, ctx : ActionContext):
        # if len(self.attack) > 0:
            # print("ENQUEUING ATTACKS")
            # print(self.attack)
        # print("-----------------")
        ctx.state.pending_attacks.extend(self.attack)

@dataclass
class ClearPendingAttacksEffect(Effect):
    
    def apply(self, ctx : ActionContext):
        ctx.pending_attacks.clear()

# ----------- damage -----------

@dataclass
class DamageEffect(Effect):
    pos : tuple[int, int]
    damage : int = 1

    def apply(self, ctx: ActionContext):
        # print("DAMAGE EFFECT")
        # print(f"pos {self.pos}, damage {self.damage}")
        unit = ctx.board.get_token(self.pos)
        # if unit is not None and self.damage > 0:
        #     unit.add_wounds(self.damage)
        if self.damage > 0:
            unit.add_wounds(self.damage)

@dataclass
class ResolveUnitsDamageEffect(Effect):
    positions: list[tuple[int, int]]
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        # print("RESOLVE UNITS DAMAGE")
        # print(f"positions {self.positions}")
        for pos in self.positions:
            token = ctx.board.get_token(pos)
            token.add_damage(sum(token.wounds))
            token.claer_wounds()
            if not token.is_alive:
                ctx.board.remove_token(pos)

# ----------- heal -----------

@dataclass
class HealEffect(Effect):
    source_pos : tuple[int, int]
    target_pos : tuple[int, int]

    def apply(self, ctx : ActionContext):
        healer = ctx.board.get_token(self.source_pos)
        target = ctx.board.get_token(self.target_pos)
        healer.add_wounds(target.pop_highest_wound())

# ----------- removing -----------

@dataclass
class DestroyEffect(Effect):
    pos: tuple[int, int]
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        
        # if ctx.board.get_token(self.pos) is not None:
        ctx.board.destroy_token(self.pos)


# ----------- unit abilitis -----------

@dataclass
class MarkAbilityUsedEffect(Effect):
    pos: tuple[int, int]

    def apply(self, ctx: ActionContext):
        # print("MARK ABILITY USED")
        token = ctx.board.get_token(self.pos)
        token.ability_used = True


@dataclass
class ResetAbilityUsedEffect(Effect):
    positions: list[tuple[int, int]]

    def apply(self, ctx: ActionContext):
        for pos in self.positions:
            token = ctx.board.get_token(pos)
            token.state.exection.used_ability = False


# ----------- activation -----------

@dataclass
class MarkActivatedUnitsEffect(Effect):
    positions : list[tuple[int, int]]
    initiative : int

    def apply(self, ctx : ActionContext):
        # if len(self.positions) > 0:
        #     print("MARK ACTIVATED UNITS")
        #     print(f"positions {self.positions}")
        for pos in self.positions:
            token = ctx.board.get_token(pos)
            token.mark_activated(self.initiative)

# ----------- workflow data -----------

@dataclass
class ClearWorkflowDataEffect(Effect):
    def apply(self, ctx):
        ctx.workflow_data = WorkflowData()

@dataclass
class ClearSelectedHandSlotEffect(Effect):
    def apply(self, ctx):
        ctx.workflow_data.slot = None

# ----------- hand -----------

@dataclass
class DrawTokensEffect(Effect):
    hand_limit: int = 3

    def apply(self, ctx: ActionContext):
        hand = ctx.player.hand
        pile = ctx.player.pile
        while hand.size < self.hand_limit and not pile.empty:
            token = pile.draw()
            hand.add(token)


@dataclass
class DrawNamedTokenEffect(Effect):
    name: str

    def apply(self, ctx: ActionContext):
        hand = ctx.player.hand
        pile = ctx.player.pile

        if self.name not in pile.tokens:
            raise ValueError(f"nie znaleziono żetonu {self.name} w stosie gracza {ctx.faction}")

        pile.tokens.remove(self.name)
        hand.add(self.name)


@dataclass
class DiscardTokenEffect(Effect):
    slot: int

    def apply(self, ctx: ActionContext):
        # print(f"DISCARD TOKEN SLOT {self.slot}")
        ctx.player.hand.remove(self.slot)
