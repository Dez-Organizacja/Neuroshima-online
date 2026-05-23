from main.actions.akcje_na_planszy import AkcjeNaPlanszy
from main.tokens.board_token import BoardToken
from main.utils.variable import *

class Board:
    BOARD_KEY = "board"
    AVAILABLE_HEXES_KEY = "available_hexes"
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
        self.tokens = {}
        
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
                    token = BoardToken(data[x][y])
                    self.tokens[tokenID] = token
                    self.board[x][y] = tokenID
                    self.where_am_i[tokenID] = (x, y)

    def export_board(self) -> list:
        data = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    data[i][j] = self.tokens[self.board[i][j]].to_json()
        return data
    
    # ----------- board state and actions -----------

    def gen_tokenID(self, pos) -> int | None:
        x, y = pos
        return self.board[x][y]
    
    def get_position(self, tokenID) -> tuple[int, int]:
        return self.where_am_i.get(tokenID)

    def get_token(self, pos) -> BoardToken:
        if not self.on_board(pos):
            return None
        x, y = pos
        return self.tokens[self.board[x][y]] if self.board[x][y] is not None else None

    # def adjacent_hexes(self, pos):
    #     if not self.on_board(pos):
    #         return []
    #     adjacents = []
    #     for diretion in self.rose.keys():
    #         neighbor = self.go(pos, diretion)
    #         if(self.on_board(neighbor)):
    #            adjacents.append(neighbor)
    #     return adjacents 

    def is_wired(self, pos) -> bool:
        if(self.is_empty(pos)):
            return False
        return self.get_token(pos).is_wired()

    def on_border(self, pos) -> bool:
        x, y = pos
        if(not self.on_board(pos)):
            return False
        cx, cy = self.CENTER
        return (abs(cx - x) > 1 or abs(cy - y) > 2)

    def is_hq(self, pos) -> bool:
        return self.get_token(pos).is_HQ() if not self.is_empty(pos) else False

    def get_token_position(self, name, fraction) -> tuple[int, int] | None:
        for pos in self.ALL_HEXES:
            token = self.get_token(pos)
            if token and token.name == name and token.fraction == fraction:
                return pos
        return None

    # ----------- placing and moving tokens ----------

    def put_token(self, pos, name, fraction = None):
        # mozna wywolac albo put_token(pos, data) albo put_token(pos, name, fraction)
        if not self.on_board(pos):
            return
        
        token = BoardToken(name, fraction)
        
        x, y = pos
        name = token.get(token.NAME)

        tokenID = self.get_new_id()
        self.tokens[tokenID] = token
        self.board[x][y] = tokenID
        self.where_am_i[tokenID] = (x, y)

    def destroy_token(self, pos):
        if not self.on_board(pos):
            return
        x, y = pos
        self.board[x][y] = None
        del self.tokens[self.board[x][y]]
        del self.where_am_i[self.board[x][y]]

    def move_token(self, old_pos, new_pos):
        if(old_pos == new_pos):
            return
        
        x1, y1 = old_pos
        x2, y2 = new_pos

        if not self.on_board(old_pos) or not self.on_board(new_pos):
            return
        
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = None
        self.where_am_i[self.board[x2][y2]] = (x2, y2)

    def rotate_token(self, pos, rotation):
        x, y = pos
        self.tokens[self.board[x][y]].rotate(rotation)

    def is_valid_target(self, pos, frakcja, czy_sztab=False):
        x, y = pos
        return not (not self.on_board(pos) or self.is_empty(pos) or self.tokens[self.board[x][y]].frakcja == frakcja or (czy_sztab and self.get_token(pos).is_HQ()))

    def is_empty(self, pos):
        return self.get_token(pos) is None

    # def deal_damage_effect(self, pos, damage, profile):
    #     if self.is_hq(pos) and not profile.can_hit_hq:
    #         return
    #     self.get_token(pos).attacked(
    #         obrazenia=damage, 
    #         kierunek=-1, 
    #         czy_blokowalny=profile.ignore_armour
    #     )

    def deal_damage(self, pos, direction, damage, blockable=False):
        if(self.is_empty(pos)):
            return
        x, y = pos
        
        self.tokens[self.board[x][y]].take_damage(direction, damage, blockable)

    def on_board(self, pos : tuple[int, int]):
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

    def eliminate_dead(self):
        for pos in self.ALL_HEXES:
            if(self.is_empty(pos)):
                continue
            if(not self.get_token(pos).is_alive()):
                self.zdejmij_zeton(pos)

    def go(self, pos, direction):
        x, y = pos
        return (x + self.rose[direction]["x"], y + self.rose[direction]["y"])
    
    def is_adjacent(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist == 2

    def print_board(self):
        # for pos in self.ALL_HEXES:

        for i in range(self.width):
            row = []
            for j in range(self.length):
                pos = (i, j)
                if(not self.on_board(pos)):
                    continue
                if(self.board[i][j] is None):
                    row.append(None)
                else:
                    # print(type(board.board[i][j]))
                    akt = self.board[i][j]
                    row.append((
                        # akt.frakcja[0], 
                        # akt.zasiecowany,
                        akt.name, 
                        akt.ROTATION,
                    ))
                    # row.append(akt.zeton_to_json())
            print(row)
            
    # def wszystkie_jednostki(self):
    #     answer = []
    #     for x in range(self.width):
    #         for y in range(self.length):
    #             if(self.is_empty((x, y))):
    #                 continue
    #             answer.append([x, y, self.board[x][y].zeton_to_json()])
    #     return answer



    # @classmethod
    # def from_dict(cls, data):
    #     obj = cls()
    #     obj.import_board(data.get(cls.BOARD_KEY, obj.board))
    #     return obj

    # def to_dict(self):
    #     data = {
    #         self.BOARD_KEY : self.export_board(),
    #     }
    #     return data

    # def not_on_bound(self, pos):
    #     if not self.on_board(pos):
    #         return False
    #     return not self.on_border(pos)

