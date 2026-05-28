from dataclasses import dataclass, field
from typing import ClassVar
from main.state.contex import ActionContext
from main.events.data import Effect
from main.workflows.data import WorkflowData
from main.tokens.abstract_token import Token


@dataclass
class DiscardTokenEffect(Effect):
    slot: int

    def apply(self, ctx: ActionContext):
        ctx.player.hand.remove(self.slot)


@dataclass
class MoveEffect(Effect):
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]

    def apply(self, ctx: ActionContext):
        ctx.board.move_token(self.from_pos, self.to_pos)


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
class DamageProfile:
    power: int = 1
    direction: int | None = None
    blockable: bool = False


@dataclass
class DamageEffect(Effect):
    pos: tuple[int, int]
    profile: DamageProfile = field(default_factory=DamageProfile)

    def apply(self, ctx: ActionContext):
        unit = ctx.board.get_token(self.pos)
        unit.take_damage(
            direction=self.profile.direction,
            damage=self.profile.power,
            blockable=self.profile.blockable,
        )


@dataclass
class RotateEffect(Effect):
    pos: tuple[int, int]
    rotation: int
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        ctx.board.rotate_token(self.pos, self.rotation)


@dataclass
class DestroyEffect(Effect):
    pos: tuple[int, int]
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        ctx.board.destroy_token(self.pos)


@dataclass
class MarkAbilityUsedEffect(Effect):
    pos: tuple[int, int]

    def apply(self, ctx: ActionContext):
        token = ctx.board.get_token(self.pos)
        token.ability_used = True


@dataclass
class ResetAbilityUsedEffect(Effect):
    positions: list[tuple[int, int]]

    def apply(self, ctx: ActionContext):
        for pos in self.positions:
            token = ctx.board.get_token(pos)
            token.ability_used = False


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
class ClearWorkflowDataEffect(Effect):
    def apply(self, ctx):
        ctx.workflow_data = WorkflowData()


@dataclass
class RemoveDeadUnitsEffect(Effect):
    positions: list[tuple[int, int]]
    recompute_passive: ClassVar[bool] = True

    def apply(self, ctx: ActionContext):
        for pos in self.positions:
            ctx.board.remove_token(pos)