import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plansza import Board
from diff import Diff
from variable import *
from zeton import Zeton

class Tests:
    def test_bitwa1(self):
        board = Board()
        zeton = {Token.FRACTION : "moloch", Token.NAME : "szturmowiec", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(3, 3, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "wartownik", Token.ROTATION : 1, Token.DAMAGE : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 1, Token.DAMAGE : 0}
        board.postaw_zeton(1, 5, zeton)

        # board.print_board()

        board.bitwa()
        output = board.wszystkie_jednostki()
        # print(output)

        correct_output = []
        correct_output.append([1, 5, {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 1, Token.DAMAGE : 0, Token.WIRED : False}])
        correct_output.append([2, 4, {Token.FRACTION : "borgo", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 2, Token.WIRED : False}])
        correct_output.append([3, 3, {Token.FRACTION : "moloch", Token.NAME : "szturmowiec", Token.ROTATION : 0, Token.DAMAGE : 1, Token.WIRED : False}])
        # print(correct_output)
        assert(Diff().compare(output, correct_output))
        # assert(output == correct_output)
    
    def test_bitwa_sieciarze_2(self):
        board = Board()
        zeton = {Token.FRACTION : "moloch", Token.NAME : "szturmowiec", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(3, 3, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "wartownik", Token.ROTATION : 1, Token.DAMAGE : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 1, Token.DAMAGE : 0}
        board.postaw_zeton(1, 5, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "sieciarz", Token.ROTATION : 3, Token.DAMAGE : 0}
        board.postaw_zeton(4, 4, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "sieciarz", Token.ROTATION : 4, Token.DAMAGE : 0}
        board.postaw_zeton(4, 2, zeton)

        board.bitwa()
        output = board.wszystkie_jednostki()

        correct_output = []
        correct_output.append([1, 5, {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 1, Token.DAMAGE : 0, Token.WIRED : False}])
        correct_output.append([2, 4, {Token.FRACTION : "borgo", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 0, Token.WIRED : False}])
        correct_output.append([4, 2, {Token.FRACTION : "borgo", Token.NAME : "sieciarz", Token.ROTATION : 4, Token.DAMAGE : 0, Token.WIRED : False}])
        
        # print(correct_output)
        assert(Diff().compare(output, correct_output))
        # assert(output == correct_output)

        assert(Diff().compare(output, correct_output))

    def test_bitwa_sieciarze_3(self):
        board = Board()
        zeton = {Token.FRACTION : "testowa", Token.NAME : "sieciarz", Token.ROTATION : 5, Token.DAMAGE : 0}
        board.postaw_zeton(3, 3, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "sieciarz", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {Token.FRACTION : "testowa", Token.NAME : "dwu-sieciarz", Token.ROTATION : 1, Token.DAMAGE : 0}
        board.postaw_zeton(1, 3, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "sieciarz", Token.ROTATION : 3, Token.DAMAGE : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(1, 5, zeton)

        zeton = {Token.FRACTION : "testowa", Token.NAME : "sieciarz", Token.ROTATION : 2, Token.DAMAGE : 0}
        board.postaw_zeton(1, 7, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "sieciarz", Token.ROTATION : 1, Token.DAMAGE : 0}
        board.postaw_zeton(2, 8, zeton)

        zeton = {Token.FRACTION : "testowa", Token.NAME : "sieciarz", Token.ROTATION : 3, Token.DAMAGE : 0}
        board.postaw_zeton(3, 7, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "opancerzonywartownik", Token.ROTATION : 2, Token.DAMAGE : 0}
        board.postaw_zeton(4, 6, zeton)

        board.bitwa()
        output = board.wszystkie_jednostki()

        correct_output = [[1, 3, {Token.FRACTION : 'testowa', Token.NAME: 'dwu-sieciarz', Token.ROTATION: 1, Token.DAMAGE: 0, Token.WIRED: False}], [1, 5, {Token.FRACTION: 'moloch', Token.NAME: 'sztab', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: True}], [1, 7, {Token.FRACTION: 'testowa', Token.NAME: 'sieciarz', Token.ROTATION: 2, Token.DAMAGE: 0, Token.WIRED: False}], [2, 2, {Token.FRACTION: 'moloch', Token.NAME: 'sieciarz', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: False}], [2, 4, {Token.FRACTION: 'moloch', Token.NAME: 'sieciarz', Token.ROTATION: 3, Token.DAMAGE: 0, Token.WIRED: False}], [2, 8, {Token.FRACTION: 'moloch', Token.NAME: 'sieciarz', Token.ROTATION: 1, Token.DAMAGE: 0, Token.WIRED: True}], [3, 3, {Token.FRACTION: 'testowa', Token.NAME: 'sieciarz', Token.ROTATION: 5, Token.DAMAGE: 0, Token.WIRED: False}], [3, 7, {Token.FRACTION: 'testowa', Token.NAME: 'sieciarz', Token.ROTATION: 3, Token.DAMAGE: 0, Token.WIRED: False}], [4, 6, {Token.FRACTION: 'moloch', Token.NAME: 'opancerzonywartownik', Token.ROTATION: 2, Token.DAMAGE: 0, Token.WIRED: True}]]       
        assert(Diff().compare(output, correct_output))

    def test_bitwa_moduly(self):
        board = Board()

        # ---- borgo ----
        zeton = {Token.FRACTION : "borgo", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(1, 1, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "super-mutant", Token.ROTATION : 2, Token.DAMAGE : 0}
        board.postaw_zeton(0, 2, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "sieciarz", Token.ROTATION : 4, Token.DAMAGE : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {Token.FRACTION : "borgo", Token.NAME : "zwiadowca", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(3, 5, zeton)


        # ---- moloch ----
        zeton = {Token.FRACTION : "moloch", Token.NAME : "sztab", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(2, 8, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "zwiadowca", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(2, 6, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "szturmowiec", Token.ROTATION : 4, Token.DAMAGE : 0}
        board.postaw_zeton(1, 7, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "oficer", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(1, 5, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "mozg", Token.ROTATION : 0, Token.DAMAGE : 0}
        board.postaw_zeton(0, 6, zeton)

        zeton = {Token.FRACTION : "moloch", Token.NAME : "lowca", Token.ROTATION : 4, Token.DAMAGE : 0}
        board.postaw_zeton(0, 4, zeton)

        board.bitwa()
        output = board.wszystkie_jednostki()

        board.print_board()
        print(output)

        # print(output)

        # for i in range(10):
        #     print("\n")

        # board.print_board()
        
        # for i in range(10):
        #     print("\n")

        correct_output = [[0, 6, {Token.FRACTION: 'moloch', Token.NAME: 'mozg', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: False}], [1, 1, {Token.FRACTION: 'borgo', Token.NAME: 'sztab', Token.ROTATION: 0, Token.DAMAGE: 6, Token.WIRED: False}], [1, 7, {Token.FRACTION: 'moloch', Token.NAME: 'szturmowiec', Token.ROTATION: 4, Token.DAMAGE: 0, Token.WIRED: False}], [2, 4, {Token.FRACTION: 'borgo', Token.NAME: 'sieciarz', Token.ROTATION: 4, Token.DAMAGE: 0, Token.WIRED: False}], [2, 6, {Token.FRACTION: 'moloch', Token.NAME: 'zwiadowca', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: False}], [2, 8, {Token.FRACTION: 'moloch', Token.NAME: 'sztab', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: False}], [3, 5, {Token.FRACTION: 'borgo', Token.NAME: 'zwiadowca', Token.ROTATION: 0, Token.DAMAGE: 0, Token.WIRED: False}]]     


        # print(correct_output)
        assert(Diff().compare(output, correct_output))
# test = Tests()
# test.test_bitwa1()