from main.state.contex import ActionContext
from main.state.serialization import Serializator

class StateViewBuilder:
    @staticmethod
    def build_hands_view(ctx : ActionContext):
        return {
            fraction : Serializator.to_dict_dataclass(ctx.player.hand)
            for fraction in ctx.state.fractions
        }

    def build(self, ctx : ActionContext):
        return {
            "fractions" : ctx.state.fractions,
            "board" : ctx.board.to_list(),
            "hands" : self.build_hands_view(ctx)
        }