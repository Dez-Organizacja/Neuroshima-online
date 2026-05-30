from main.workflows.providers.base import WorkflowActionProvider
from main.board.board_query import BoardQuery
from main.state.contex import ActionContext
from main.input.data import Button
from main.rules.predicates import (
    token_predicate,
    is_empty_at,
    NOT
)

class HealersProvider(WorkflowActionProvider):
    
    def get_available_buttons(self, ctx : ActionContext) -> list[Button]:
        if ctx.workflow_data.unit_pos:
            return [Button.CANCEL]

        return []
    
    def get_sources(self, ctx : ActionContext) -> list[tuple[int, int]]:
        positions = BoardQuery(
            NOT(is_empty_at),
            token_predicate()
        )

    def get_available_positions(self, 
                                ctx : ActionContext
        ) -> list[tuple[int, int]]: