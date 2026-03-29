from zeton import Zeton

class Board:
    def __init__(self):
        self.length = 9
        self.width = 5
        self.board = [[None] * self.length for i in range(self.width)]
        
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

    def obruc(self, x, y, rotacja):
        self.board[x][y].obruc(rotacja)

    def import_board(self, data):
        for x in range(self.width):
            for y in range(self.length):
                pole = data[x][y]
                if(pole is None):
                    self.board[x][y] = None
                else:
                    self.postaw_zeton(x, y, pole)

    def is_empty(self, x, y):
        return (self.board[x][y] == None)

    def board_to_json(self):
        json_board = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    json_board[i][j] = self.board[i][j].zeton_to_json()
        return json_board