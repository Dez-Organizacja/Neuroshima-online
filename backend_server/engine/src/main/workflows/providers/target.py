from main.workflows.providers.base import WorkflowActionProvider
from abc import ABC, abstractmethod
from main.input.data import Button
from main.board.query import BoardQuery
import main.rules.predicates as pr
from main.state.contex import ActionContext

def is_full_bomb_center(board, pos):
    return board.on_board(pos) and len(board.adjacent_hexes(pos)) == 6

class TargetProvider(ABC, WorkflowActionProvider):
    def get_available_buttons(self, ctx : ActionContext):
        return [Button.CANCEL, Button.DISCARD]
    
    @abstractmethod
    def get_available_targets(self, ctx : ActionContext):
        pass

    def get_available_positions(self, ctx):
        return self.get_available_targets(ctx)

class SniperProvider(TargetProvider):
    def get_available_targets(self, ctx : ActionContext):
        query = BoardQuery([
            pr.NOT(pr.token_predicate(lambda t: t.wired)),
            pr.NOT(pr.token_predicate(lambda t: t.is_HQ)),
            pr.is_enemy(ctx.faction)
        ])
        return query.apply(ctx.board)

class BombProvider(TargetProvider):
    def get_available_targets(self, ctx : ActionContext):
        query = BoardQuery([
            is_full_bomb_center,
        ])
        return query.apply(ctx.board)

class GrenadeProvider(TargetProvider):
    @staticmethod
    def get_available_targets(ctx : ActionContext):
        pos = ctx.board.get_hq_pos(ctx.faction)
        if pos is None:
            return []

        hq = ctx.board.get_token(pos)
        if hq.wired:
            return []

        return BoardQuery([
            pr.adjacent_to(pos),
            pr.is_enemy_of(hq),
            pr.NOT(pr.token_predicate(lambda t: t.wired)),
            pr.NOT(pr.token_predicate(lambda t: t.is_HQ)),
        ]).apply(ctx.board)
