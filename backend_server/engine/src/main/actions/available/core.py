from main.actions.available.data import AvailableStructure
from main.actions.available.config import AvailableActionProvider
from main.state.contex import ActionContext
from main.input.data import Button, UserAction
from main.rules.place import PlacementRules
from main.tokens.token_factory import TokenFactory
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
            decision_faction : str | None = None,
        ) -> AvailableStructure:
        # print(f"provider {provider}")
        # print(f"board function {provider.get_positions}")
        # print(f"board {provider.get_positions(ctx)}")
        # print(f"buttons function {provider.get_buttons}")
        # print(f"buttons {provider.get_buttons(ctx)}")
        actions : AvailableStructure = AvailableStructure()
        actions.board = provider.get_positions(ctx)
        actions.buttons = provider.get_buttons(ctx)

        if ctx.player.hand.size == 3:
            actions.buttons = [
                button for button in actions.buttons
                if button != Button.END_TURN
            ]
        if ctx.player.hand.size == 3 and ctx.workflow_data.slot is not None:
            token_name = ctx.player.hand.get(ctx.workflow_data.slot)
            if token_name is not None:
                token = TokenFactory.create(token_name, faction=ctx.faction)
                actions.board = []
                actions.buttons = []
                if PlacementRules.can_discard(token):
                    actions.buttons = [Button.DISCARD]

        if ctx.state.can_undo(decision_faction) and Button.CANCEL not in actions.buttons:
            actions.buttons.append(Button.CANCEL)
        cls.apply_hand(actions.hand, provider.get_tokens(ctx))
        return actions
