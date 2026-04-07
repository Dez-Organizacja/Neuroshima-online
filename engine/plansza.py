from zeton import Zeton

class Board:
    def __init__(self):
        self.length = 9
        self.width = 5
        self.rotation_phase = False
        self.board = [[None] * self.length for i in range(self.width)]
        self.available_hexs = [[False] * self.length for i in range(self.width)]
        
        self.roza = {
            0: [-1, 1],
            1: [0, 2],
            2: [1, 1],
            3: [1, -1],
            4: [0, -2],
            5: [-1, -1]
        }

    def postaw_zeton(self, x, y, zeton):
        self.board[x][y] = Zeton(x, y, zeton["frakcja"], zeton["nazwa"], zeton["rotacja"], zeton["rany"])
        # self.rotation_phase = True

    def rotate(self, x, y, rotacja):
        self.board[x][y].rotate(rotacja)

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