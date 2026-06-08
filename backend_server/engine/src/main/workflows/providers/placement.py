from main.workflows.providers.base import WorkflowActionProvider
from main.input.data import Button
from main.state.contex import ActionContext
from main.board.query import BoardQuery
from main.rules.predicates import is_empty_at
from main.rules.place import PlacementRules
from main.tokens.token_factory import TokenFactory

class PlacementProvider(WorkflowActionProvider):
    def get_available_buttons(self, ctx : ActionContext):
        result = [Button.CANCEL]
        token_name = ctx.player.hand.get(ctx.workflow_data.slot)
        token = TokenFactory.create(token_name, faction=ctx.faction)
        if PlacementRules.can_discard(token):
            result.append(Button.DISCARD)
        return result
    
    def get_available_positions(self, ctx : ActionContext):
        # print("available positions")
        # print(BoardQuery([is_empty_at]).apply(ctx))
        return BoardQuery([is_empty_at]).apply(ctx.board)