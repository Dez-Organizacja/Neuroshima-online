from sieciarze import sieciarze
from zeton import Zeton
from variable import *

class Board:
    def __init__(self):
        self.length = 9
        self.width = 5
        self.rotation_phase = False
        self.board = [[None] * self.length for i in range(self.width)]
        self.available_hexs = [[False] * self.length for i in range(self.width)]
        self.max_inicjatywa = 10
        self.ALL_HEXES = [(x, y) for y in range(self.length) for x in range(self.width)]
        self.CENTER = (self.width // 2, self.length // 2)

        self.roza = {
            0 : {"x" : -1, "y" : 1},
            1 : {"x" : 0, "y" : 2},
            2 : {"x" : 1, "y" : 1},
            3 : {"x" : 1, "y" : -1},
            4 : {"x" : 0, "y" : -2},
            5 : {"x" : -1, "y" : -1},
        }

    def adjacent_hexes(self, x, y):
        adjacents = []
        for diretion in self.roza.keys():
            nx, ny = self.go(x, y, diretion)
            if(self.on_board(nx, ny)):
               adjacents.append((nx, ny))
        return adjacents 

    def dist_to_centre(self, x, y):
        cx = self.width // 2
        cy = self.length // 2
        dist = (abs(x - cx) + abs(y - cy))
        if(dist % 2):
            dist = 100
        return dist

    def is_on_bound(self, x, y):
        if(not self.on_board(x, y)):
            return False
        cx, cy = self.CENTER
        return (abs(cx - x) <= 1 and abs(cy - y) <= 2)

    def find_zeton(self, nazwa, frakcja):
        for x in range(self.width):
            for y in range(self.length):
                pole = self.board[x][y]
                if(pole is None):
                    continue
                if(pole.nazwa == nazwa and pole.frakcja == frakcja):
                    return (x, y)
        return None

    def postaw_zeton(self, x, y, zeton):
        self.board[x][y] = Zeton(x, y, zeton)
        # self.rotation_phase = True

    def rotate(self, x, y, rotacja):
        self.board[x][y].rotate(rotacja)

    def get_name(self, x, y):
        if(self.is_empty(x, y)):
            return None
        return self.board[x][y].nazwa

    def is_valid_target(self, x, y, frakcja, czy_sztab=False):
        if (not self.is_index_on_board(x, y)):
            return False
        if(not self.on_board(x, y)):
            return False
        if(self.is_empty(x, y)):
            return False
        if(self.get_type(x, y) == frakcja):
            return False
        if(czy_sztab and self.get_name(x, y) == "sztab"):
            return False
        return True

    def is_empty(self, x, y):
        return (self.board[x][y] == None)

    def is_index_on_board(self, x, y):
        return (0 <= x < self.width and 0 <= y < self.length)

    def on_board(self, x, y):
        if(not isinstance(x, int)):
            return False
        if(not isinstance(y, int)):
            return False
        
        return self.dist_to_centre(x, y) <= 4

    def get_type(self, x, y):
        if(not self.on_board(x, y)):
            return None
        if(self.board[x][y] is None):
            return None
        return self.board[x][y].frakcja

    def update_available_hexs(self, types, hexes, function):
        for x in range(self.width):
            for y in range(self.length):
                type = self.get_type(x, y)
                if(types != Variable.ALL and type not in types):
                    self.available_hexs[x][y] = False
                    continue
                
                if((x, y) not in hexes):
                    self.available_hexs[x][y] = False
                    continue

                if(function is None):
                    self.available_hexs[x][y] = True
                    continue
                
                else:
                    self.available_hexs[x][y] = function(x, y)

    def boost_all(self):
        for x in range(self.width):
            for y in range(self.length):
                if(self.is_empty(x, y)):
                    continue
                self.board[x][y].boost(self)

    def bitwa(self):
        for inicjatywa in range(self.max_inicjatywa, -1, -1):
            print(f"--- Inicjatywa {inicjatywa} ---")

            self.kwestia_sieciarzy()
            self.boost_all()

            self.print_board()

            for x in range(self.width):
                for y in range(self.length):
                    if(self.is_empty(x, y)):
                        continue
                    self.board[x][y].activate(self, inicjatywa)
            
            for x in range(self.width):
                for y in range(self.length):
                    if(self.is_empty(x, y)):
                        continue
                    if(not self.board[x][y].koniec_inicjatywy()):
                        self.board[x][y] = None
    
    def kwestia_sieciarzy(self):
        self.sieciarze = sieciarze()
        self.sieciarze.kwestia_sieciarzy(self)

    def go(self, x, y, direction):
        return (x + self.roza[direction]["x"], y + self.roza[direction]["y"])

    def print_board(self):
        for i in range(self.width):
            row = []
            for j in range(self.length):
                if(self.board[i][j] is None):
                    row.append(None)
                else:
                    # print(type(board.board[i][j]))
                    akt = self.board[i][j]
                    row.append((
                        # akt.frakcja[0], 
                        akt.zasiecowany,
                        akt.nazwa, 
                        akt.rotacja
                    ))
                    # row.append(akt.zeton_to_json())
            print(row)

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

    def board_to_json(self):
        json_board = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    json_board[i][j] = self.board[i][j].zeton_to_json()
        return json_board