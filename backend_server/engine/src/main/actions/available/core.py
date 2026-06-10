from main.actions.available.data import AvailableStructure
from main.actions.available.config import AvailableActionProvider
from main.state.contex import ActionContext
from main.input.data import UserAction
from typing import TypeVar
A = TypeVar("A", bound=UserAction)

class AvailableActions:
    @staticmethod
    def apply_hand(hand, hand_result):
        for idx in hand_result:
            hand[idx] = True

    @classmethod
    def get_actions(
            cls, 
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
        cls.apply_hand(actions.hand, provider.get_tokens(ctx))
        return actions