from main.state.contex import ActionContext
from main.state.serialization import Serializator

class StateViewBuilder:
    @staticmethod
    def build_hands_view(ctx : ActionContext):
        return {
            faction : Serializator.to_dict_dataclass(ctx.player.hand)
            for faction in ctx.state.factions
        }

    def build(self, ctx : ActionContext):
        return {
            "factions" : ctx.state.factions,
            "board" : ctx.board.to_list(),
            "hands" : self.build_hands_view(ctx)
        }