from akcje_na_planszy import AkcjeNaPlanszy
from sieciarze import Sieciarze
from zeton import Zeton
from variable import *

class Board:
    BOARD_KEY = "board"
    # AVAILABLE_HEXES_KEY = "available_hexes"
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
        # self.available_hexs = [[False] * self.length for i in range(self.width)]
        self.ALL_HEXES = []
        for x in range(self.width):
            for y in range(self.length):
                if(self.on_board(x, y)):
                    self.ALL_HEXES.append((x, y))
                    
        self.max_inicjatywa = 10


    def adjacent_hexes(self, x, y):
        adjacents = []
        for diretion in self.roza.keys():
            nx, ny = self.go(x, y, diretion)
            if(self.on_board(nx, ny)):
               adjacents.append((nx, ny))
        return adjacents 

    def is_on_bound(self, x, y):
        if(not self.on_board(x, y)):
            return False
        cx, cy = self.CENTER
        return (abs(cx - x) > 1 or abs(cy - y) > 2)

    def not_on_bound(self, x, y):
        return (not self.is_on_bound(x, y))

    def find_zeton(self, nazwa, frakcja):
        for x in range(self.width):
            for y in range(self.length):
                pole = self.board[x][y]
                if(pole is None):
                    continue
                if(pole.nazwa == nazwa and pole.frakcja == frakcja):
                    return self.board[x][y]
        return None

    def not_is_hq(self, x, y):
        if(self.is_empty(x, y)):
            return True
        return (self.board[x][y].nazwa != Token.Type.Board.HQ)

    def postaw_zeton(self, x, y, zeton):
        self.board[x][y] = Zeton(x, y, zeton)
        # self.rotation_phase = True

    def zdejmij_zeton(self, x, y):
        self.board[x][y] = None

    def przenies(self, x, y, nx, ny):
        if(x == nx and y == ny):
            return
        self.board[nx][ny] = self.board[x][y]
        self.board[x][y] = None

    def rotate(self, x, y, rotacja):
        self.board[x][y].rotate(rotacja)

    def get_name(self, x, y):
        if(self.is_empty(x, y)):
            return None
        return self.board[x][y].nazwa

    def is_valid_target(self, x, y, frakcja, czy_sztab=False):
        # if (not self.is_index_on_board(x, y)):
        #     return False

        print(f"valid target: ({x},{y}), frakcja {frakcja}, frakcja2 {self.get_type(x, y)}, czy_sztab {czy_sztab}")

        if(not self.on_board(x, y)):
            return False
        if(self.is_empty(x, y)):
            return False
        if(self.board[x][y].frakcja == frakcja):
            return False
        if(czy_sztab and self.get_name(x, y) == "sztab"):
            return False
        return True

    def is_empty(self, x, y):
        return (self.board[x][y] == None)

    # def is_index_on_board(self, x, y):
    #     return (0 <= x < self.width and 0 <= y < self.length)

    def deal_damage(self, x, y, damage):
        if(self.is_empty(x, y)):
            return
        self.board[x][y].dostan_rane(damage)

    def on_board(self, x, y):
        if(not isinstance(x, int)):
            return False
        if(not isinstance(y, int)):
            return False
        
        cx, cy = self.CENTER
        dx = abs(x - cx)
        dy = abs(y - cy)
        if(dx > 2 or dy > 4):
            return False
        
        d = dx + dy
        if(d % 2 or d > 4):
            return False
        
        # print("on board")
        # print(x, y)
        return True

    def get_type(self, x, y):
        if(not self.on_board(x, y)):
            return None
        if(self.board[x][y] is None):
            return None
        return self.board[x][y].frakcja

    def can_move(self, x, y):
        if(not self.on_board(x, y)):
            return False
        if(self.is_empty(x, y)):
            return False
        if(self.board[x][y].czy_zasieciowany()):
            return False
        
        for hex in self.adjacent_hexes(x, y):
            nx, ny = hex
            if(self.is_empty(nx, ny)):
                return True
        return False

    def boost_all(self):
        for x in range(self.width):
            for y in range(self.length):
                if(self.is_empty(x, y)):
                    continue
                self.board[x][y].boost(self)

    def check_hex(self, x, y):
        if(self.board[x][y].is_empty()):
            return True
        return self.board[x][y].is_alive()

    def zdejmij_trupy(self):
        for x in range(self.width):
            for y in range(self.length):
                if(self.is_empty(x, y)):
                    continue
                if(not self.board[x][y].is_alive()):
                    self.zdejmij_zeton(x, y)

    def bitwa(self):
        for inicjatywa in range(self.max_inicjatywa, -1, -1):
            print(f"--- Inicjatywa {inicjatywa} ---")

            anp = AkcjeNaPlanszy(self)

            anp.reset_all()
            anp.kwestia_sieciarzy()
            anp.boost_all()
            anp.aktywacja(inicjatywa)
            self.zdejmij_trupy()

    def go(self, x, y, direction):
        return (x + self.roza[direction]["x"], y + self.roza[direction]["y"])
    
    def is_adjacent(self, x1, y1, x2, y2):
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist == 2

    def can_be_pushed(self, px, py, x, y):
        if(self.is_empty(x, y)):
            return False
        if(self.board[x][y].czy_zasieciowany()):
            return False
        
        pusher_adj = self.adjacent_hexes(px, py)
        my_adj = self.adjacent_hexes(x, y)
        for hex in my_adj:
            if(hex not in pusher_adj):
                return True
        return False

    def can_push(self, x, y):
        if(self.is_empty(x, y)):
            return False
        if(self.board[x][y].czy_zasieciowany()):
            return False
        
        for hex in self.adjacent_hexes(x, y):
            nx, ny = hex
            if(self.can_be_pushed(x, y, nx, ny)):
                return True
        return False

    def print_board(self):
        for i in range(self.width):
            row = []
            for j in range(self.length):
                if(not self.on_board(i, j)):
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

    def czy_w_planszy(self, x, y):
        return (0 <= x < 5 and 0 <= y < 9)

    def wszystkie_jednostki(self):
        answer = []
        for x in range(self.width):
            for y in range(self.length):
                if(self.is_empty(x, y)):
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
                    self.postaw_zeton(x, y, pole) 

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
        obj.available_hexs = data.get(cls.AVAILABLE_HEXES_KEY, obj.available_hexs)
        return obj


    def to_dict(self):
        data = {
            self.BOARD_KEY : self.export_board(),
            self.AVAILABLE_HEXES_KEY : self.available_hexs
        }
        return data