from dataclasses import dataclass
from main.tokens.board_token import BoardToken, TokenView

Hex = tuple[int, int]

@dataclass
class Tile:
    pos : Hex
    unit : BoardToken 

@dataclass
class TileView:
    pos : Hex
    unit : TokenView