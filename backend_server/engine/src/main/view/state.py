from main.state.contex import ActionContext
from main.state.serialization import Serializator
from main.board.board import TileView

class StateViewBuilder:
    @staticmethod
    def build_hands_view(ctx : ActionContext):
        return {
            faction : Serializator.to_dict_dataclass(player_state.hand)
            for faction, player_state in ctx.state.players.items()
        }

    def build_board_view(self, ctx : ActionContext):
        tiles = [
            TileView(pos=tile.pos, unit=tile.unit)
            for tile in ctx.board.get_tiles()
        ]

        return [
            Serializator.to_dict_dataclass(tile)
            for tile in tiles
        ]

    def build(self, ctx : ActionContext):
        return {
            "factions" : ctx.state.factions,
            "board" : self.build_board_view(ctx),
            "hands" : self.build_hands_view(ctx)
        }