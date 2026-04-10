import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from akcje import Actions
from main import Game
from plansza import Board
from diff import Diff

class DummyGame:
    def __init__(self):
        board = Board()
        pass
        # self.bottoms = ["koniec tury", "kosz", "użyj", "cancel", "tak", "nie"]

class Test_board:
    def test_on_board(self):
        board = Board()
        assert (board.on_board(0, 8) == False)
        assert (board.on_board(2, 4) == True)
        assert (board.on_board(3, 0) == False)

    def fill_board(self, board):
        zeton = {"nazwa" : "klaun", "frakcja" : "moloch", "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {"nazwa" : "szturmowiec", "frakcja" : "moloch", "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(2, 2,zeton)

        zeton = {"nazwa" : "wartownik", "frakcja" : "moloch", "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(0, 2, zeton)

        zeton = {"nazwa" : "mutek", "frakcja" : "borgo", "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(1, 1,zeton)

        zeton = {"nazwa" : "mutek", "frakcja" : "borgo", "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(4, 2,zeton)

        zeton = {"nazwa" : "sztab", "frakcja" : "borgo", "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(3, 3, zeton)


    def test_available_hexes1(self):
        board = Board()
        self.fill_board(board)

        board.update_available_hexs([None, "moloch"], board.ALL_HEXES, None)
        correct_output = [[True] * board.length for i in range(board.width)]
        correct_output[1][1] = False
        correct_output[4][2] = False
        correct_output[3][3] = False
        assert(Diff().compare(board.available_hexs, correct_output))

    def test_available_hexes2(self):
        board = Board()
        self.fill_board(board)

        x, y = board.find_zeton("sztab", "borgo")
        board.update_available_hexs(["moloch"], board.adjacent_hexes(x, y), None)
        # print(board.available_hexs)
        correct_output = [[False] * board.length for i in range(board.width)]
        correct_output[2][2] = True
        correct_output[2][4] = True
        assert(Diff().compare(board.available_hexs, correct_output))

    def test_available_hexes3(self):
        board = Board()
        self.fill_board(board)
        board.update_available_hexs(["moloch", "borgo", None], board.ALL_HEXES, board.is_on_bound)        
    
        correct_output = [[False] * board.length for i in range(board.width)]
        correct_output[1][3] = True
        correct_output[1][5] = True
        correct_output[2][2] = True
        correct_output[2][4] = True
        correct_output[2][6] = True
        correct_output[3][3] = True
        correct_output[3][5] = True
        assert(Diff().compare(board.available_hexs, correct_output))


    # def test_start(self):
    #     data = {
    #         "faza": "newgame",
    #         "frakcje": {
    #             "player1": "borgo",
    #             "player2": "moloch"
    #         }
    #     }

    #     game = Game(data)
    #     self.output = game.export_game_state()
    #     # print(self.output)

    #     poprawne = {}
    #     poprawne["faza"] = "sztaby"
    #     poprawne["next_turns"] = [{"frakcja" : "borgo", "typ" : "wystaw_sztab"}, {"frakcja" : "moloch", "typ" : "wystaw_sztab"}, {'frakcja': 'bitwa', 'typ': 'ostatnia'}]
    #     poprawne["current_frakcja"] = "borgo"
    #     poprawne["user_actions"] = []
    #     poprawne["board"] = [[None for _ in range(9)] for _ in range(5)]
    #     # trzeba nanosic kazda zmiane, bo moga zmieniac poprawne z zmiana koncepji
    #     assert (self.output["board"] == poprawne["board"])
    #     assert (self.output["current_frakcja"] == "borgo")


    # def run_wstawianie(self, board, action, nazwa, frakcja, expected):
    #     akcje = Actions(DummyGame())
    #     hand = [nazwa, "a", "b"]
    #     previous_board = [[board.get_type(x, y) for y in range(board.length)] for x in range(board.width)]
    #     # print("Previous board:")
    #     # for row in previous_board:
    #     #     print(row)

    #     status = akcje.wstawianie(board, hand, action, nazwa, frakcja)

    #     assert (status == expected)

    #     if(status):
    #         ax = action["x"]
    #         ay = action["y"]
    #         assert (board.get_type(ax, ay) == frakcja)
    #         zeton = board.board[ax][ay]
    #         assert (zeton.nazwa == nazwa)
    #         assert (zeton.frakcja == frakcja)
    #         assert (zeton.rany == 0)
    #         assert (zeton.rotacja == 0)
    #         for x in range(board.width):
    #             for y in range(board.length):
    #                 if(x == ax and y == ay):
    #                     continue
    #                 assert (board.get_type(x, y) == previous_board[x][y])
        
    #     else:
    #         for x in range(board.width):
    #             for y in range(board.length):
    #                 assert (board.get_type(x, y) == previous_board[x][y])
                    
    #     return status

    # def test_wstawianie(self):
    #     board = Board()
    #     frakcja = "moloch"
    #     nazwa = "sieciarz"
    #     action = {"x": 1, "y": 7}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, True) == True)
        
    #     nazwa = "klaun"
    #     action = {"x": 5, "y": 7}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, False) == False)

    #     action = {"x": 1, "y": 7}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, False) == False)
    
    #     frakcja = "borgo"
    #     nazwa = "mutek"
    #     action = {"x": 2, "y": 2}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, True) == True)

    #     frakcja = "moloch"
    #     nazwa = "bloker"
    #     action = {"x": 2, "y": 2}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, False) == False)