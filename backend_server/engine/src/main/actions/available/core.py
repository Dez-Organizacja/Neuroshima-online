from main.actions.available.data import AvailableStructure
from main.actions.available.config import AvailableActionProvider
from main.actions.available.builder import AvailableActionsBuilder
from main.state.contex import ActionContext
from main.input.data import UserAction
from typing import TypeVar
A = TypeVar("A", bound=UserAction)

class AvailableActions:
    def __init__(self, provider : AvailableActionProvider):
        self.builder = AvailableActionsBuilder()
        self.provider = provider

    def apply_hand(self, hand, hand_result):
        for idx in hand_result:
            hand[idx] = True

    def get_actions(self, ctx : ActionContext) -> AvailableStructure:
        actions : AvailableStructure = AvailableStructure()
        actions.board = self.provider.get_positions(ctx)
        actions.buttons = self.provider.get_buttons(ctx)
        self.apply_hand(actions.hand, self.provider.get_tokens(ctx))
        return actions