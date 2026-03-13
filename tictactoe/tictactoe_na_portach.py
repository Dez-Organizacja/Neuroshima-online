from panda3d.core import TransparencyAttrib, LineSegs, NodePath
from direct.showbase.MessengerGlobal import messenger
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

import socket
import json

class TicTacToe(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.board_size = 3
        self.current_player = 1
        self.game_over = False
        self.used = []

        self.HOST = "127.0.0.1"
        self.PORT = 9000

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        self.client.setblocking(False)

        self.buffer = ""

        self.radius = 2

        self.status = OnscreenText(text=f"Current Player: {self.current_player}", pos=(0, 0.9), scale=0.06, fg=(1, 1, 1, 1))
        self.grid_node = self.aspect2d.attachNewNode('grid')

        self.setBackgroundColor(0.2, 0.2, 0.2, 1)
        self.draw_board()

        self.taskMgr.add(self.listen_server, "listen_server")

        self.accept('opp-move', self.oponent_move)
        self.accept('mouse1', self.on_click)
        self.accept('reset-game', self.reset_local)
        self.accept('r', self.reset_game)

    def draw_board(self):
        lines = LineSegs()
        lines.setThickness(2)
        lines.setColor(1, 1, 1, 1)

        cell_size = 0.5
        half = (self.board_size * cell_size) / 2
        self.half_cell = cell_size / 2

        for i in range(1, 3):
            x = -half + i * cell_size
            lines.moveTo(x, 0, -half)
            lines.drawTo(x, 0, half)

        for i in range(1, 3):
            z = -half + i * cell_size
            lines.moveTo(-half, 0, z)
            lines.drawTo(half, 0, z)

        node = lines.create()
        nodepath = NodePath(node)
        nodepath.reparentTo(self.grid_node)

        self.board_coords = [[0 for _ in range(3)] for _ in range(3)] # to jest srodek pola, border +- 0.25
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = -half + col * cell_size + cell_size / 2
                z = -half + row * cell_size + cell_size / 2

                self.board_coords[row][col] = (x, z)

    def on_click(self):
        if self.game_over or not self.mouseWatcherNode.hasMouse() or self.current_player == 2:
            return

        m = self.mouseWatcherNode.getMouse()
        mx = m.getX() * self.getAspectRatio()
        my = m.getY()

        for row in range(self.board_size):
            for col in range(self.board_size):
                x, y = self.board_coords[row][col]
                x1, x2, y1, y2 = x - self.half_cell, x + self.half_cell, y - self.half_cell, y + self.half_cell

                if x1 <= mx <= x2 and y1 <= my <= y2:
                    # print(f"Checking cell ({row}, {col}): x1={x1}, x2={x2}, y1={y1}, y2={y2}, click=({mx}, {my})")
                    
                    if self.board[row][col] is None:
                        self.board[row][col] = self.current_player
                        self.draw_mark(row, col, self.current_player)

                        data = {
                            "action": "move",
                            "row": row,
                            "col": col
                        }

                        self.client.send((json.dumps(data) + "\n").encode())

                        if self.check_win():
                            self.status.setText(f"You Won!")
                            self.game_over = True
                            return


                        self.current_player = 2

        self.status.setText(f"Your oponent's turn...")   

    def reset_game(self):
        data = {
            "action": "reset",
        }
        self.client.send((json.dumps(data) + '\n').encode())

        for cell in self.used:
            cell.removeNode()
        self.used = []

        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 1
        self.game_over = False

        if self.current_player == 1: 
            self.status.setText(f"Your turn!")
        else:
            self.status.setText(f"Your oponent's turn...")

    def reset_local(self):
        for cell in self.used:
            cell.removeNode()
        self.used = []

        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 1
        self.game_over = False

        if self.current_player == 1: 
            self.status.setText(f"Your turn!")
        else:
            self.status.setText(f"Your oponent's turn...")

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
    
    def draw_mark(self, row, col, player):
        x, z = self.board_coords[row][col]
        scale = self.half_cell * 0.8

        img_file = "x.png" if player == 1 else "o.png"
        img = OnscreenImage(image=img_file, pos=(x, 0, z), scale=scale)
        img.setTransparency(TransparencyAttrib.MAlpha)
        img.reparentTo(self.grid_node)

        self.used.append(img)

    def listen_server(self, task):
        try:
            data = self.client.recv(1024)

            if data:
                self.buffer += data.decode()

                while "\n" in self.buffer:
                    line, self.buffer = self.buffer.split("\n", 1)

                    if not line.strip():
                        continue

                    message = json.loads(line)

                    if message["action"] == "move":
                        messenger.send("opp-move", [message])

                    if message["action"] == "reset":
                        messenger.send("reset-game")

        except BlockingIOError:
            pass

        return task.cont
    
    def oponent_move(self, data):
        x = data.get("row")
        y = data.get("col")

        self.current_player = 1

        if self.board[x][y] is None:
            self.board[x][y] = 2
            self.draw_mark(x, y, 2)

        if (self.check_win()):
            self.status.setText(f"You lost!")
            self.game_over = True
            return
        
        self.status.setText(f"Your turn!")


game = TicTacToe()
game.run()