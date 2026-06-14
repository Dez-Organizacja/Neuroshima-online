from main.state.game_state import GameState
from main.state.serialization import Serializator
from main.board.board import TileView

class StateViewBuilder:
    @staticmethod
    def build_hands_view(state : GameState):
        return {
            faction : Serializator.to_dict_dataclass(player_state.hand)
            for faction, player_state in state.players.items()
        }

    @staticmethod
    def build_board_view(state : GameState):

        tiles = [
            TileView(pos=tile.pos, unit=tile.unit.get_view())
            for tile in state.board.get_tiles()
        ]
        # print("TILES")
        # print(tiles)
        # print("---------------")

        return [
            Serializator.to_dict_dataclass(tile)
            for tile in tiles
        ]
    
    @staticmethod
    def build_piles_view(state : GameState):
        return {
            faction : state.players[faction].pile.size
            for faction in state.factions
        }

    @classmethod
    def build(cls, state : GameState):
        return {
            "factions" : state.factions,
            "board" : cls.build_board_view(state),
            "hands" : cls.build_hands_view(state),
            "piles" : cls.build_piles_view(state),
        }