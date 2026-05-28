from main.actions.available.data import AvailableStructure
from main.state.contex import ActionContext
from main.input.data import Button

class AvailableActionsBuilder:
    @staticmethod
    def build_hand(ctx : ActionContext):
        return {
            faction: [False for _ in range(player.hand.size)]
            for faction, player in ctx.state.players.items()
        }         

    def build_buttons(ctx : ActionContext):
        return {
            button: False
            for button in Button
        }

    def build(self, ctx : ActionContext):
        return AvailableStructure(
            hand=self.build_hand(ctx),
            buttons=self.build_buttons(ctx)
        )