from main.tokens.board_token import BoardToken
from main.tokens.data import BoardType
from main.utils.variable import *
from dataclasses import dataclass
from main.state.serialization import Serializator
from main.tokens.token_factory import TokenFactory
from main.tokens.data import TokenView

Hex = tuple[int, int]

@dataclass
class Tile:
    pos : Hex
    unit : BoardToken 

@dataclass
class TileView:
    pos : Hex
    unit : TokenView

class Board:
    length = 9
    width = 5
    rose = {
        0 : {"x" : -1, "y" : 1},
        1 : {"x" : 0, "y" : 2},
        2 : {"x" : 1, "y" : 1},
        3 : {"x" : 1, "y" : -1},
        4 : {"x" : 0, "y" : -2},
        5 : {"x" : -1, "y" : -1},
    }
    CENTER = (width // 2, length // 2)
    max_inicjatywa = 10
    last_id = 0

    def __init__(self):
        self.board = [[None] * self.length for i in range(self.width)]
        self.where_am_i : dict[int, tuple[int, int]] = {}
        self.tokens : dict[int, BoardToken] = {}
        
        self.ALL_HEXES = []

        for x in range(self.width):
            for y in range(self.length):
                if(self.on_board((x, y))):
                    self.ALL_HEXES.append((x, y))

    # ----------- import/export -----------

    def get_new_id(self) -> int:
        self.last_id += 1
        return self.last_id

    def import_board(self, data) -> None:
        self.board = [[None] * self.length for _ in range(self.width)]
        self.where_am_i = {}
        self.tokens = {}
        self.last_id = 0

        for x in range(self.width):
            for y in range(self.length):
                if(data[x][y] is None):
                    self.board[x][y] = None
                else:
                    tokenID = self.get_new_id()
                    token = BoardToken.from_dict(data[x][y])
                    self.tokens[tokenID] = token
                    self.board[x][y] = tokenID
                    self.where_am_i[tokenID] = (x, y)

    def export_board(self) -> list:
        data = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    data[i][j] = self.tokens[self.board[i][j]].to_dict()
        return data
    
    # ----------- board state and actions -----------

    def gen_tokenID(self, pos : Hex) -> int | None:
        x, y = pos
        return self.board[x][y]
    
    def get_position(self, tokenID) -> tuple[int, int]:
        return self.where_am_i.get(tokenID)

    def remove_token(self, pos : Hex):
        if not self.on_board(pos):
            return
        x, y = pos
        del self.tokens[self.board[x][y]]
        del self.where_am_i[self.board[x][y]]
        self.board[x][y] = None

    def get_token(self, pos : Hex) -> BoardToken:
        if not self.on_board(pos):
            return None
        x, y = pos
        return self.tokens[self.board[x][y]] if self.board[x][y] is not None else None

    def get_token_position(self, name, faction) -> tuple[int, int] | None:
        for pos in self.ALL_HEXES:
            token = self.get_token(pos)
            if token and token.name == name and token.faction == faction:
                return pos
        return None
    
    def get_hq_pos(self, faction) -> tuple[int, int] | None:
        return self.get_token_position(name=BoardType.HQ.value, faction=faction)

    def get_line(self, pos : Hex, direction : int) -> list[Hex]:
        line = []
        while self.on_board(pos):
            line.append(pos)
            pos = self.go(pos, direction)

        return line
    
    def adjacent_hexes(self, pos : Hex):
        if not self.on_board(pos):
            return []
        adjacents = []
        for diretion in self.rose.keys():
            neighbor = self.go(pos, diretion)
            if(self.on_board(neighbor)):
               adjacents.append(neighbor)
        return adjacents 
    
    def on_border(self, pos : Hex) -> bool:
        x, y = pos
        if(not self.on_board(pos)):
            return False
        cx, cy = self.CENTER
        return (abs(cx - x) > 1 or abs(cy - y) > 2)
    # ----------- placing and moving tokens ----------

    def add_token(self, pos : Hex, token : BoardToken):
        # print("ADD TOKEN")
        # print(token)
        # print(f"pos {pos}")
        # print("--------------")
        x, y = pos
        tokenID = self.get_new_id()
        self.tokens[tokenID] = token
        self.board[x][y] = tokenID
        self.where_am_i[tokenID] = pos

    def import_token(self, pos : Hex, data : dict):
        token = data if isinstance(data, BoardToken) else BoardToken.from_dict(data)
        self.add_token(pos, token)

    def put_token(self, pos : Hex, name, faction = None):
        # mozna wywolac albo put_token(pos, data) albo put_token(pos, name, faction)
        if not self.on_board(pos):
            return
        
        token = TokenFactory.create(name, faction)
        self.add_token(pos, token)

    def destroy_token(self, pos : Hex):
        self.remove_token(pos)

    def move_token(self, old_pos : Hex, new_pos : Hex):
        if(old_pos == new_pos):
            return
        
        x1, y1 = old_pos
        x2, y2 = new_pos

        if not self.on_board(old_pos) or not self.on_board(new_pos):
            return
        
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = None
        self.where_am_i[self.board[x2][y2]] = (x2, y2)

    def rotate_token(self, pos : Hex, rotation : int):
        x, y = pos
        self.tokens[self.board[x][y]].rotate(rotation)

    def is_valid_target(self, pos : Hex, frakcja : str, czy_sztab : bool=False):
        x, y = pos
        return not (not self.on_board(pos) or self.is_empty(pos) or self.tokens[self.board[x][y]].faction == frakcja or (czy_sztab and self.get_token(pos).is_HQ()))

    def is_empty(self, pos : Hex):
        return self.get_token(pos) is None

    def on_board(self, pos : Hex):
        x, y = pos
        cx, cy = self.CENTER
        dx = abs(x - cx)
        dy = abs(y - cy)
        if(dx > 2 or dy > 4):
            return False
        
        d = dx + dy
        if(d % 2 or d > 4):
            return False
        
        return True

    def go(self, pos : Hex, direction : int):
        x, y = pos
        return (x + self.rose[direction]["x"], y + self.rose[direction]["y"])
    
    def is_adjacent(self, pos1 : Hex, pos2 : Hex):
        x1, y1 = pos1
        x2, y2 = pos2
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist == 2

    def get_tiles(self) -> list[Tile]:
        return [
            Tile(
                    pos=self.where_am_i[id],
                    unit=token
                )
            for id, token in self.tokens.items()
        ]

    @classmethod
    def from_list(cls, data : list) -> Board:
        obj = cls()
        for tile_data in data:
            tile : Tile = Serializator.from_dict_dataclass(Tile, tile_data)
            obj.import_token(tile.pos, tile.unit)

        return obj

    def to_list(self) -> list:
        return [
            Serializator.to_dict_dataclass(tile)
            for tile in self.get_tiles()
        ]
