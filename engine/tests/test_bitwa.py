import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plansza import Board
from diff import Diff

class Tests:
    def test_bitwa1(self):
        board = Board()
        zeton = {"frakcja" : "moloch", "nazwa" : "szturmowiec", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(3, 3, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "wartownik", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(1, 5, zeton)

        # board.print_board()

        board.bitwa()
        output = board.wszystkie_jednostki()
        # print(output)

        correct_output = []
        correct_output.append([1, 5, {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 1, "rany" : 0, "zasiecowany" : False}])
        correct_output.append([2, 4, {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 2, "zasiecowany" : False}])
        correct_output.append([3, 3, {"frakcja" : "moloch", "nazwa" : "szturmowiec", "rotacja" : 0, "rany" : 1, "zasiecowany" : False}])
        # print(correct_output)
        assert(Diff().compare(output, correct_output))
        # assert(output == correct_output)
    
    def test_bitwa_sieciarze_2(self):
        board = Board()
        zeton = {"frakcja" : "moloch", "nazwa" : "szturmowiec", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(3, 3, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "wartownik", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(1, 5, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "sieciarz", "rotacja" : 3, "rany" : 0}
        board.postaw_zeton(4, 4, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "sieciarz", "rotacja" : 4, "rany" : 0}
        board.postaw_zeton(4, 2, zeton)

        board.bitwa()
        output = board.wszystkie_jednostki()

        correct_output = []
        correct_output.append([1, 5, {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 1, "rany" : 0, "zasiecowany" : False}])
        correct_output.append([2, 4, {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0, "zasiecowany" : False}])
        correct_output.append([4, 2, {"frakcja" : "borgo", "nazwa" : "sieciarz", "rotacja" : 4, "rany" : 0, "zasiecowany" : False}])

        assert(Diff().compare(output, correct_output))

    def test_bitwa_sieciarze_3(self):
        board = Board()
        zeton = {"frakcja" : "testowa", "nazwa" : "sieciarz", "rotacja" : 5, "rany" : 0}
        board.postaw_zeton(3, 3, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sieciarz", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {"frakcja" : "testowa", "nazwa" : "dwu-sieciarz", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(1, 3, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sieciarz", "rotacja" : 3, "rany" : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(1, 5, zeton)

        zeton = {"frakcja" : "testowa", "nazwa" : "sieciarz", "rotacja" : 2, "rany" : 0}
        board.postaw_zeton(1, 7, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sieciarz", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(2, 8, zeton)

        zeton = {"frakcja" : "testowa", "nazwa" : "sieciarz", "rotacja" : 3, "rany" : 0}
        board.postaw_zeton(3, 7, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "opancerzonywartownik", "rotacja" : 2, "rany" : 0}
        board.postaw_zeton(4, 6, zeton)

        board.bitwa()
        output = board.wszystkie_jednostki()

        correct_output = [[1, 3, {'frakcja': 'testowa', 'nazwa': 'dwu-sieciarz', 'rotacja': 1, 'rany': 0, 'zasiecowany': False}], [1, 5, {'frakcja': 'moloch', 'nazwa': 'sztab', 'rotacja': 0, 'rany': 0, 'zasiecowany': True}], [1, 7, {'frakcja': 'testowa', 'nazwa': 'sieciarz', 'rotacja': 2, 'rany': 0, 'zasiecowany': False}], [2, 2, {'frakcja': 'moloch', 'nazwa': 'sieciarz', 'rotacja': 0, 'rany': 0, 'zasiecowany': False}], [2, 4, {'frakcja': 'moloch', 'nazwa': 'sieciarz', 'rotacja': 3, 'rany': 0, 'zasiecowany': False}], [2, 8, {'frakcja': 'moloch', 'nazwa': 'sieciarz', 'rotacja': 1, 'rany': 0, 'zasiecowany': True}], [3, 3, {'frakcja': 'testowa', 'nazwa': 'sieciarz', 'rotacja': 5, 'rany': 0, 'zasiecowany': False}], [3, 7, {'frakcja': 'testowa', 'nazwa': 'sieciarz', 'rotacja': 3, 'rany': 0, 'zasiecowany': False}], [4, 6, {'frakcja': 'moloch', 'nazwa': 'opancerzonywartownik', 'rotacja': 2, 'rany': 0, 'zasiecowany': True}]]       
        assert(Diff().compare(output, correct_output))

    def test_bitwa_moduly(self):
        board = Board()

        # ---- borgo ----
        zeton = {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(1, 1, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "super-mutant", "rotacja" : 2, "rany" : 0}
        board.postaw_zeton(0, 2, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "sieciarz", "rotacja" : 4, "rany" : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "zwiadowca", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(3, 5, zeton)


        # ---- moloch ----
        zeton = {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(2, 8, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "zwiadowca", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(2, 6, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "szturmowiec", "rotacja" : 4, "rany" : 0}
        board.postaw_zeton(1, 7, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "oficer", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(1, 5, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "mozg", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(0, 6, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "lowca", "rotacja" : 4, "rany" : 0}
        board.postaw_zeton(0, 4, zeton)

        board.bitwa()
        output = board.wszystkie_jednostki()

        board.print_board()
        print(output)

        correct_output = [[0, 6, {'frakcja': 'moloch', 'nazwa': 'mozg', 'rotacja': 0, 'rany': 0, 'zasiecowany': False}], [1, 1, {'frakcja': 'borgo', 'nazwa': 'sztab', 'rotacja': 0, 'rany': 6, 'zasiecowany': False}], [1, 7, {'frakcja': 'moloch', 'nazwa': 'szturmowiec', 'rotacja': 4, 'rany': 0, 'zasiecowany': False}], [2, 4, {'frakcja': 'borgo', 'nazwa': 'sieciarz', 'rotacja': 4, 'rany': 0, 'zasiecowany': False}], [2, 6, {'frakcja': 'moloch', 'nazwa': 'zwiadowca', 'rotacja': 0, 'rany': 0, 'zasiecowany': False}], [2, 8, {'frakcja': 'moloch', 'nazwa': 'sztab', 'rotacja': 0, 'rany': 0, 'zasiecowany': False}], [3, 5, {'frakcja': 'borgo', 'nazwa': 'zwiadowca', 'rotacja': 0, 'rany': 0, 'zasiecowany': False}]]
        assert(Diff().compare(output, correct_output))
# test = Tests()
# test.test_bitwa1()