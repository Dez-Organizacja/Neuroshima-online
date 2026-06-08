from main.workflows.providers.base import WorkflowActionProvider
from abc import ABC, abstractmethod
from main.input.data import Button
from main.board.query import BoardQuery
import main.rules.predicates as pr
from main.state.contex import ActionContext
from main.tokens.board_token import BoardToken

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
            pr.NOT(pr.token_predicate(BoardToken.is_wired)),
            pr.is_enemy(ctx.faction)
        ])
        return query.apply(ctx.board)

class BombProvider(TargetProvider):
    def get_available_targets(self, ctx : ActionContext):
        query = BoardQuery([pr.NOT(pr.is_on_border)])
        return query.apply(ctx.board)

class GrenadeProvider(TargetProvider):
    @staticmethod
    def get_available_targets(ctx : ActionContext):
        pos = ctx.board.get_hq_pos(ctx.faction)
        hq = ctx.board.get_token(pos)
        if hq.is_wired():
            return []

        return BoardQuery([
            pr.adjacent_to(pos),
            pr.is_enemy_of(hq),
            pr.NOT(pr.token_predicate(BoardToken.is_wired))
        ]).apply(ctx.board)