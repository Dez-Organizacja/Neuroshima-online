from main.actions.akcje_na_planszy import AkcjeNaPlanszy
from main.tokens.board_token import BoardToken
from main.utils.variable import *

class Board:
    BOARD_KEY = "board"
    AVAILABLE_HEXES_KEY = "available_hexes"
    length = 9
    width = 5
    roza = {
        0 : {"x" : -1, "y" : 1},
        1 : {"x" : 0, "y" : 2},
        2 : {"x" : 1, "y" : 1},
        3 : {"x" : 1, "y" : -1},
        4 : {"x" : 0, "y" : -2},
        5 : {"x" : -1, "y" : -1},
    }
    CENTER = (width // 2, length // 2)

    def __init__(self):
        self.board = [[None] * self.length for i in range(self.width)]
        self.ALL_HEXES = []
        for x in range(self.width):
            for y in range(self.length):
                if(self.on_board((x, y))):
                    self.ALL_HEXES.append((x, y))
                    
        self.max_inicjatywa = 10

    def get_tile(self, pos) -> BoardToken:
        if not self.on_board(pos):
            return None
        x, y = pos
        return self.board[x][y]
    
    def assign_to_tile(self, pos, new_tile):    
        x, y = pos
        self.board[x][y] = new_tile


    def adjacent_hexes(self, pos):
        if not self.on_board(pos):
            return []
        adjacents = []
        for diretion in self.roza.keys():
            neighbor = self.go(pos, diretion)
            if(self.on_board(neighbor)):
               adjacents.append(neighbor)
        return adjacents 

    def is_wired(self, pos):
        if(self.is_empty(pos)):
            return False
        return self.get_tile(pos).czy_zasiecowany()

    def on_border(self, pos):
        x, y = pos
        if(not self.on_board(pos)):
            return False
        cx, cy = self.CENTER
        return (abs(cx - x) > 1 or abs(cy - y) > 2)

    def is_hq_wired(self, fraction):
        tile = self.get_tile(self.get_token_position(BoardType.HQ, fraction))
        return (tile and not tile.czy_zasieciowany())

    def is_hq(self, pos):
        return self.get_name(pos) == BoardType.HQ.value

    def get_hq_pos(self, fraction):
        return self.get_token_position(BoardType.HQ, fraction) 
    
    def get_token_position(self, name, fraction):
        expected_name = name.value if isinstance(name, BoardType) else name
        for pos in self.ALL_HEXES:
            tile = self.get_tile(pos)
            if tile and tile.name == expected_name and tile.fraction == fraction:
                return pos
        return None

    def find_zeton(self, nazwa, frakcja):
        for x in range(self.width):
            for y in range(self.length):
                pole = self.board[x][y]
                if(pole is None):
                    continue
                if(pole.nazwa == nazwa and pole.frakcja == frakcja):
                    return self.board[x][y]
        return None

    def postaw_zeton(self, pos, zeton):
        if not self.on_board(pos):
            return
        x, y = pos
        name = zeton.get(Token.NAME)
        fraction = zeton.get(Token.FRACTION)
        data = {**zeton, Token.X: x, Token.Y: y}
        self.board[x][y] = BoardToken(name, fraction, data)
        # self.rotation_phase = True

    def zdejmij_zeton(self, pos):
        if not self.on_board(pos):
            return
        x, y = pos
        self.board[x][y] = None

    def destroy(self, pos):
        self.zdejmij_zeton(pos)

    def move(self, old_pos, new_pos):
        if(old_pos == new_pos):
            return
        self.assign_to_tile(new_pos, self.get_tile(old_pos))
        self.assign_to_tile(old_pos, None)

    def rotate(self, pos, rotacja):
        x, y = pos
        self.board[x][y].rotate(rotacja)
    
    def is_valid_target(self, pos, frakcja, czy_sztab=False):
        if(not self.on_board(pos)):
            return False
        if(self.is_empty(pos)):
            return False
        x, y = pos
        if(self.board[x][y].frakcja == frakcja):
            return False
        if(czy_sztab and self.get_name(pos) == "sztab"):
            return False
        return True

    def is_empty(self, pos):
        return self.get_tile(pos) is None

    def deal_damage_effect(self, pos, damage, profile):
        if self.is_hq(pos) and not profile.can_hit_hq:
            return
        self.get_tile(pos).attacked(
            obrazenia=damage, 
            kierunek=-1, 
            czy_blokowalny=profile.ignore_armour
        )

    def deal_damage(self, pos, damage):
        if(self.is_empty(pos)):
            return
        x, y = pos
        self.board[x][y].dostan_rane(damage)

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
    
    def get_type(self, pos):
        if(not self.on_board(pos)):
            return None
        if(self.is_empty(pos)):
            return None
        return self.get_tile(pos).fraction

    def zdejmij_trupy(self):
        for pos in self.ALL_HEXES:
            if(self.is_empty(pos)):
                continue
            if(not self.get_tile(pos).is_alive()):
                self.zdejmij_zeton(pos)

    def bitwa(self):
        for inicjatywa in range(self.max_inicjatywa, -1, -1):
            print(f"--- Inicjatywa {inicjatywa} ---")

            anp = AkcjeNaPlanszy(self)

            anp.reset_all()
            anp.kwestia_sieciarzy()
            anp.stealing_boosts()
            anp.boost_all()
            anp.aktywacja(inicjatywa)
            self.zdejmij_trupy()

    def go(self, pos, direction):
        x, y = pos
        return (x + self.roza[direction]["x"], y + self.roza[direction]["y"])
    
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
                        akt.nazwa, 
                        akt.rotacja
                    ))
                    # row.append(akt.zeton_to_json())
            print(row)
            
    def wszystkie_jednostki(self):
        answer = []
        for x in range(self.width):
            for y in range(self.length):
                if(self.is_empty((x, y))):
                    continue
                answer.append([x, y, self.board[x][y].zeton_to_json()])
        return answer

    def import_board(self, data):
        for x in range(self.width):
            for y in range(self.length):
                pole = data[x][y]
                if(pole is None):
                    self.board[x][y] = None
                else:
                    self.postaw_zeton((x, y), pole) 

    def export_board(self):
        data = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    data[i][j] = self.board[i][j].zeton_to_json()
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.import_board(data.get(cls.BOARD_KEY, obj.board))
        return obj

    def to_dict(self):
        data = {
            self.BOARD_KEY : self.export_board(),
        }
        return data

    def not_on_bound(self, pos):
        if not self.on_board(pos):
            return False
        return not self.on_border(pos)

    def czy_w_planszy(self, pos):
        return self.on_board(pos)
