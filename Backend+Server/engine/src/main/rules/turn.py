from main.state.contex import ActionContext
from main.board.board_query import BoardQuery
from main.rules.predicates import is_empty_at

class TurnRules:
    @staticmethod
    def can_end(ctx : ActionContext) -> bool:
        return True
    
    @staticmethod
    def end_turn_check(ctx : ActionContext) -> bool:
        return any(BoardQuery([is_empty_at]).apply(ctx))