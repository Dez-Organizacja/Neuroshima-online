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

    def apply_active_keys(self, dict, keys):
        for key in keys:
            dict[key] = True

    def apply_hand(self, hand, hand_result):
        for fraction, idxes in hand_result.items():
            for i in idxes:
                hand[fraction][i] = True

    def get_actions(self, ctx : ActionContext) -> AvailableStructure:
        actions = AvailableStructure.build(ctx)
        self.apply_active_keys(actions.board, self.provider.get_positions(ctx))
        self.apply_active_keys(actions.bottoms, self.provider.get_bottoms(ctx))
        self.apply_hand(self.provider.get_tokens(ctx))
        return actions