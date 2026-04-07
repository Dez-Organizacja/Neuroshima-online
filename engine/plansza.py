from zeton import Zeton

class Board:
    def __init__(self):
        self.length = 9
        self.width = 5
        self.rotation_phase = False
        self.board = [[None] * self.length for i in range(self.width)]
        self.available_hexs = [[False] * self.length for i in range(self.width)]
        self.max_inicjatywa = 10

        self.roza = {
            0 : {"x" : 1, "y" : 1},
            1 : {"x" : 0, "y" : 2},
            2 : {"x" : -1, "y" : 1},
            3 : {"x" : -1, "y" : -1},
            4 : {"x" : 0, "y" : -2},
            5 : {"x" : 1, "y" : -1},
        }

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

    def on_board(self, x, y):
        if(not isinstance(x, int)):
            return False
        if(x < 0 or x >= self.width):
            return False
        if(not isinstance(y, int)):
            return False
        if(y < 0 or y >= self.length):
            return False
        return True  

    def get_type(self, x, y):
        if(not self.on_board(x, y)):
            return None
        if(self.board[x][y] is None):
            return None
        return self.board[x][y].frakcja

    def update_available_hexs(self, type):
        if(isinstance(type, bool)):
            for x in range(self.width):
                for y in range(self.length):
                    self.available_hexs[x][y] = type
            return
        
        for x in range(self.width):
            for y in range(self.length):
                if(self.get_type(x, y) == type):
                    self.available_hexs[x][y] = True
                else:
                    self.available_hexs[x][y] = False
        
        if(isinstance(type, dict)):
            self.available_hexs[type["x"]][type["y"]] = "rotate" 

    def bitwa(self):
        for inicjatywa in range(self.max_inicjatywa, -1, -1):
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
                    row.append((self.board[i][j].nazwa, self.board[i][j].rotacja))
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