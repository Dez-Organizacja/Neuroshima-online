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
        board.import_token((2, 4), {"name": "sieciarz", "faction": "moloch", "rotation": 1, "damage": 0})

        board.import_token((0, 4), {"name": "sieciarz", "faction": "moloch", "rotation": 3, "damage": 0})

        # [0]
        board.import_token((1, 3), {"name": "sieciarz", "faction": "testowa", "rotation": 2, "damage": 0})

        board.import_token((2, 6), {"name": "sieciarz", "faction": "testowa", "rotation": 0, "damage": 0})

        board.import_token((1, 5), {"name": "sieciarz", "faction": "testowa", "rotation": 5, "damage": 0})

        # pop = defaultdict(int, {(2, 4): 1, (0, 4): 1, (1, 5): 1, (1, 3): 1, (2, 6): 2})
        pop = {(2, 4): 1, (0, 4): 1, (1, 5): 1, (1, 3): 1, (2, 6): 2}
        
        sieciarze = Sieciarze(board)
        sieciarze.kwestia_sieciarzy()

        data = sieciarze.status_sieciarzy

        assert data == pop

        board.import_token((1, 1), {"name": "sieciarz", "faction": "moloch", "rotation": 1, "damage": 0})

        # pop = defaultdict(int, {(1, 1): 1, (2, 4): 1, (0, 4): 1, (1, 5): 2, (1, 3): 2, (2, 6): 2})
        pop = {(1, 1): 1, (2, 4): 1, (0, 4): 1, (1, 5): 2, (1, 3): 2, (2, 6): 2}
        
        sieciarze = Sieciarze(board)
        sieciarze.kwestia_sieciarzy()

        data = sieciarze.status_sieciarzy

        assert data == pop

    # def test_sieciarze2(self):
    #     board = Board()
        
    #     zeton = {"faction" : "testowa", "name" : "sieciarz", "ROTATION" : 5, "DAMAGE" : 0}
    #     board.import_token((3, 3), zeton)

    #     zeton = {"faction" : "moloch", "name" : "sieciarz", "ROTATION" : 0, "DAMAGE" : 0}
    #     board.import_token((2, 2), zeton)

    #     zeton = {"faction" : "testowa", "name" : "dwu-sieciarz", "ROTATION" : 1, "DAMAGE" : 0}
    #     board.import_token((1, 3), zeton)

    #     zeton = {"faction" : "moloch", "name" : "sieciarz", "ROTATION" : 3, "DAMAGE" : 0}
    #     board.import_token((2, 4), zeton)

    #     zeton = {"faction" : "moloch", "name" : "sztab", "ROTATION" : 0, "DAMAGE" : 0}
    #     board.import_token((1, 5), zeton)

    #     zeton = {"faction" : "testowa", "name" : "sieciarz", "ROTATION" : 2, "DAMAGE" : 0}
    #     board.import_token((1, 7), zeton)

    #     zeton = {"faction" : "moloch", "name" : "sieciarz", "ROTATION" : 1, "DAMAGE" : 0}
    #     board.import_token((2, 8), zeton)

    #     zeton = {"faction" : "testowa", "name" : "sieciarz", "ROTATION" : 3, "DAMAGE" : 0}
    #     board.import_token((3, 7), zeton)

    #     zeton = {"faction" : "moloch", "name" : "opancerzonywartownik", "ROTATION" : 2, "DAMAGE" : 0}
    #     board.import_token((4, 6), zeton)

    #     sieciarze = Sieciarze(board)
    #     sieciarze.kwestia_sieciarzy()

    #     out = sieciarze.status_sieciarzy

    #     cout = {(1, 3): 1, (1, 5): 2, (1, 7): 1, (2, 2): 1, (2, 4): 1, (2, 8): 2, (3, 3): 1, (3, 7): 1, (4, 6): 2}

    #     # correct_output = [[1, 3, {Token.FACTION : 'testowa', Token.NAME: 'dwu-sieciarz', Token.rotation: 1, Token.damage: 0, Token.wired: False}], [1, 5, {Token.FACTION: 'moloch', Token.NAME: 'sztab', Token.rotation: 0, Token.damage: 0, Token.wired: True}], [1, 7, {Token.FACTION: 'testowa', Token.NAME: 'sieciarz', Token.rotation: 2, Token.damage: 0, Token.wired: False}], [2, 2, {Token.FACTION: 'moloch', Token.NAME: 'sieciarz', Token.rotation: 0, Token.damage: 0, Token.wired: False}], [2, 4, {Token.FACTION: 'moloch', Token.NAME: 'sieciarz', Token.rotation: 3, Token.damage: 0, Token.wired: False}], [2, 8, {Token.FACTION: 'moloch', Token.NAME: 'sieciarz', Token.rotation: 1, Token.damage: 0, Token.wired: True}], [3, 3, {Token.FACTION: 'testowa', Token.NAME: 'sieciarz', Token.rotation: 5, Token.damage: 0, Token.wired: False}], [3, 7, {Token.FACTION: 'testowa', Token.NAME: 'sieciarz', Token.rotation: 3, Token.damage: 0, Token.wired: False}], [4, 6, {Token.FACTION: 'moloch', Token.NAME: 'opancerzonywartownik', Token.rotation: 2, Token.damage: 0, Token.wired: True}]]       
    #     assert out == cout
