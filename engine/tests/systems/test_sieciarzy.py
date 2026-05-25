from collections import defaultdict
from main.board.board import Board
from main.systems import sieciarze
from main.tokens.board_token import BoardToken
from main.tokens.data import Token
from main.utils.variable import *
from main.systems.sieciarze import Sieciarze

# from plansza import Board

class TestSieciarze:
    def test_sieciarze1(self):
        board = Board()

        # [0, 5]
        board.import_token((2, 4), {"name": "sieciarz", "fraction": "moloch", "ROTATION": 1, "DAMAGE": 0})

        board.import_token((0, 4), {"name": "sieciarz", "fraction": "moloch", "ROTATION": 3, "DAMAGE": 0})

        # [0]
        board.import_token((1, 3), {"name": "sieciarz", "fraction": "testowa", "ROTATION": 2, "DAMAGE": 0})

        board.import_token((2, 6), {"name": "sieciarz", "fraction": "testowa", "ROTATION": 0, "DAMAGE": 0})

        board.import_token((1, 5), {"name": "sieciarz", "fraction": "testowa", "ROTATION": 5, "DAMAGE": 0})

        # pop = defaultdict(int, {(2, 4): 1, (0, 4): 1, (1, 5): 1, (1, 3): 1, (2, 6): 2})
        pop = {(2, 4): 1, (0, 4): 1, (1, 5): 1, (1, 3): 1, (2, 6): 2}
        
        sieciarze = Sieciarze(board)
        sieciarze.kwestia_sieciarzy()

        data = sieciarze.status_sieciarzy

        assert data == pop

        board.import_token((1, 1), {"name": "sieciarz", "fraction": "moloch", "ROTATION": 1, "DAMAGE": 0})

        # pop = defaultdict(int, {(1, 1): 1, (2, 4): 1, (0, 4): 1, (1, 5): 2, (1, 3): 2, (2, 6): 2})
        pop = {(1, 1): 1, (2, 4): 1, (0, 4): 1, (1, 5): 2, (1, 3): 2, (2, 6): 2}
        
        sieciarze = Sieciarze(board)
        sieciarze.kwestia_sieciarzy()

        data = sieciarze.status_sieciarzy

        assert data == pop

    # def test_sieciarze2(self):
    #     board = Board()
        
    #     zeton = {"fraction" : "testowa", "name" : "sieciarz", "ROTATION" : 5, "DAMAGE" : 0}
    #     board.import_token((3, 3), zeton)

    #     zeton = {"fraction" : "moloch", "name" : "sieciarz", "ROTATION" : 0, "DAMAGE" : 0}
    #     board.import_token((2, 2), zeton)

    #     zeton = {"fraction" : "testowa", "name" : "dwu-sieciarz", "ROTATION" : 1, "DAMAGE" : 0}
    #     board.import_token((1, 3), zeton)

    #     zeton = {"fraction" : "moloch", "name" : "sieciarz", "ROTATION" : 3, "DAMAGE" : 0}
    #     board.import_token((2, 4), zeton)

    #     zeton = {"fraction" : "moloch", "name" : "sztab", "ROTATION" : 0, "DAMAGE" : 0}
    #     board.import_token((1, 5), zeton)

    #     zeton = {"fraction" : "testowa", "name" : "sieciarz", "ROTATION" : 2, "DAMAGE" : 0}
    #     board.import_token((1, 7), zeton)

    #     zeton = {"fraction" : "moloch", "name" : "sieciarz", "ROTATION" : 1, "DAMAGE" : 0}
    #     board.import_token((2, 8), zeton)

    #     zeton = {"fraction" : "testowa", "name" : "sieciarz", "ROTATION" : 3, "DAMAGE" : 0}
    #     board.import_token((3, 7), zeton)

    #     zeton = {"fraction" : "moloch", "name" : "opancerzonywartownik", "ROTATION" : 2, "DAMAGE" : 0}
    #     board.import_token((4, 6), zeton)

    #     sieciarze = Sieciarze(board)
    #     sieciarze.kwestia_sieciarzy()

    #     out = sieciarze.status_sieciarzy

    #     cout = {(1, 3): 1, (1, 5): 2, (1, 7): 1, (2, 2): 1, (2, 4): 1, (2, 8): 2, (3, 3): 1, (3, 7): 1, (4, 6): 2}

    #     # correct_output = [[1, 3, {Token.FRACTION : 'testowa', Token.NAME: 'dwu-sieciarz', Token.ROTATION: 1, Token.DAMAGE: 0, Token.WIRED: False}], [1, 5, {Token.FRACTION: 'moloch', Token.NAME: 'sztab', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: True}], [1, 7, {Token.FRACTION: 'testowa', Token.NAME: 'sieciarz', Token.ROTATION: 2, Token.DAMAGE: 0, Token.WIRED: False}], [2, 2, {Token.FRACTION: 'moloch', Token.NAME: 'sieciarz', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: False}], [2, 4, {Token.FRACTION: 'moloch', Token.NAME: 'sieciarz', Token.ROTATION: 3, Token.DAMAGE: 0, Token.WIRED: False}], [2, 8, {Token.FRACTION: 'moloch', Token.NAME: 'sieciarz', Token.ROTATION: 1, Token.DAMAGE: 0, Token.WIRED: True}], [3, 3, {Token.FRACTION: 'testowa', Token.NAME: 'sieciarz', Token.ROTATION: 5, Token.DAMAGE: 0, Token.WIRED: False}], [3, 7, {Token.FRACTION: 'testowa', Token.NAME: 'sieciarz', Token.ROTATION: 3, Token.DAMAGE: 0, Token.WIRED: False}], [4, 6, {Token.FRACTION: 'moloch', Token.NAME: 'opancerzonywartownik', Token.ROTATION: 2, Token.DAMAGE: 0, Token.WIRED: True}]]       
    #     assert out == cout