import main.rules.predicates as pr
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.utils.variable import Bottom

class MoveRules:
    @staticmethod
    def can_move(ctx : ActionContext, pos):
        for hex in ctx.board.adjacent_hexes(pos):
            if pr.is_empty_at(ctx, hex):
                return True
        return False
    
    def get_available_sources(self, ctx : ActionContext):
        candiates = BoardQuery([
            pr.is_ally_at,
            pr.NOT(pr.is_wired_at)
        ]).apply(ctx)
        return [p for p in candiates if self.can_move(ctx, p)]


    def get_available_destinations(self, ctx : ActionContext, unit_pos):
        result = BoardQuery([
            pr.is_empty_at,
            pr.adjacent_to(unit_pos)
        ]).apply(ctx)
        return result + [unit_pos]