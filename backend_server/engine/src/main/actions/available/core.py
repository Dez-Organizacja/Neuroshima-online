from main.actions.available.data import AvailableStructure
from main.actions.available.config import AvailableActionProvider
from main.actions.available.builder import AvailableActionsBuilder
from main.state.contex import ActionContext
from main.input.data import UserAction
from typing import TypeVar
A = TypeVar("A", bound=UserAction)

class AvailableActions:
    def __init__(self):
        self.builder = AvailableActionsBuilder()

    def apply_hand(self, hand, hand_result):
        for idx in hand_result:
            hand[idx] = True

    def get_actions(
            self, 
            ctx : ActionContext,
            provider : AvailableActionProvider,
        ) -> AvailableStructure:
        # print(f"provider {provider}")
        # print(f"board function {provider.get_positions}")
        # print(f"board {provider.get_positions(ctx)}")
        # print(f"buttons function {provider.get_buttons}")
        # print(f"buttons {provider.get_buttons(ctx)}")
        actions : AvailableStructure = AvailableStructure()
        actions.board = provider.get_positions(ctx)
        actions.buttons = provider.get_buttons(ctx)
        self.apply_hand(actions.hand, provider.get_tokens(ctx))
        return actions