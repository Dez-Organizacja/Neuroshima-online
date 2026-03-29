from panda3d.core import TransparencyAttrib, LineSegs, NodePath
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from random import randint

class TicTacToe(ShowBase):
    def __init__(self, board_size=3):
        super().__init__()
        self.disableMouse()
        self.board_size = 3

        self.restart_settings()

        self.radius = 2

        self.status = OnscreenText(text=f"Current Player: {self.current_player}", pos=(0, 0.9), scale=0.06, fg=(1, 1, 1, 1))
        self.grid_node = self.aspect2d.attachNewNode('grid')

        self.setBackgroundColor(0.2, 0.2, 0.2, 1)
        self.draw_board()

        self.accept('escape', self.exit_game)
        self.accept('mouse1', self.on_click)
        self.accept('r', self.reset_game)
        self.taskMgr.add(self.game_loop, "game_loop")

    def draw_board(self):
        lines = LineSegs()
        lines.setThickness(2)
        lines.setColor(1, 1, 1, 1)

        cell_size = 0.5
        half = (self.board_size * cell_size) / 2
        self.half_cell = cell_size / 2

        for i in range(1, self.board_size):
            x = -half + i * cell_size
            lines.moveTo(x, 0, -half)
            lines.drawTo(x, 0, half)

        for i in range(1, self.board_size):
            z = -half + i * cell_size
            lines.moveTo(-half, 0, z)
            lines.drawTo(half, 0, z)

        node = lines.create()
        nodepath = NodePath(node)
        nodepath.reparentTo(self.grid_node)

        self.board_coords = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)] # to jest srodek pola, border +- 0.25
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = -half + col * cell_size + cell_size / 2
                z = -half + row * cell_size + cell_size / 2

                self.board_coords[row][col] = (x, z)
                if not self.board[row][col] == None:
                    self.draw_mark(row, col, self.board[row][col])

    def draw_mark(self, row, col, player):
        self.board[row][col] = player
        x, z = self.board_coords[row][col]
        scale = self.half_cell * 0.8

        img_file = "x.png" if player == 1 else "o.png"
        img = OnscreenImage(image=img_file, pos=(x, 0, z), scale=scale)
        img.setTransparency(TransparencyAttrib.MAlpha)
        img.reparentTo(self.grid_node)

        self.used.append(img)

    def game_loop(self, task):
        if not self.game_over:
            if self.current_player == 2:
                self.bot()

        return task.cont

    def make_move(self, row, col):
        self.draw_mark(row, col, self.current_player)

        if self.check_end():
            self.end_game()
            return

        self.current_player = 2 if self.current_player == 1 else 1

    def on_click(self):
        if self.game_over:
            return
        
        if not self.mouseWatcherNode.hasMouse():
            return

        if not self.current_player == 1:
            return

        m = self.mouseWatcherNode.getMouse()
        mx = m.getX() * self.getAspectRatio()
        my = m.getY()

        for row in range(self.board_size):
            for col in range(self.board_size):
                x, y = self.board_coords[row][col]
                x1, x2, y1, y2 = x - self.half_cell, x + self.half_cell, y - self.half_cell, y + self.half_cell

                if x1 <= mx <= x2 and y1 <= my <= y2:
                    print(f"Checking cell ({row}, {col}): x1={x1}, x2={x2}, y1={y1}, y2={y2}, click=({mx}, {my})")
                    
                    if self.board[row][col] is None:
                        self.make_move(row, col)
                        if(self.game_over):
                            return

        self.status.setText(f"Current: Player {self.current_player}")   
 
    def bot(self):
        row = randint(0, self.board_size - 1)
        col = randint(0, self.board_size - 1)
        while self.board[row][col] is not None:
            row = randint(0, self.board_size - 1)
            col = randint(0, self.board_size - 1)
        
        self.make_move(row, col)

    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != None:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != None:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != None:
            return True

        return False

    def check_draw(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == None:
                    return False
        return True

    def check_end(self):
        if self.check_win():
            self.winner = self.current_player
            return True

        if self.check_draw():
            return True

        return False

    def end_game(self):
        if not self.winner == 0:
            self.status.setText(f"Player {self.current_player} wins! Press R to reset.")
        else:
            self.status.setText("Draw; Press R to reset.")
        self.game_over = True

    def restart_settings(self):
        self.used = []
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = randint(1, 2)
        self.winner = 0
        self.game_over = False

    def reset_game(self):
        for cell in self.used:
            cell.removeNode()

        self.restart_settings()
        self.status.setText(f"Current Player: {self.current_player}")

    def exit_game(self):
        self.userExit()

game = TicTacToe()
game.run()