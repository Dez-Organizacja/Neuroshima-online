import pytest
from plansza import Board
from diff import Diff

class Tests:
    def test_bitwa1(self):
        board = Board()
        zeton = {"frakcja" : "moloch", "nazwa" : "szturmowiec", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(1, 3, zeton)

        zeton = {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 0}
        board.postaw_zeton(2, 4, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "wartownik", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(2, 2, zeton)

        zeton = {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 1, "rany" : 0}
        board.postaw_zeton(3, 5, zeton)

        # board.print_board()

        board.bitwa()
        output = board.wszystkie_jednostki()
        # print(output)

        correct_output = []
        correct_output.append([1, 3, {"frakcja" : "moloch", "nazwa" : "szturmowiec", "rotacja" : 0, "rany" : 1}])
        correct_output.append([2, 4, {"frakcja" : "borgo", "nazwa" : "sztab", "rotacja" : 0, "rany" : 3}])
        correct_output.append([3, 5, {"frakcja" : "moloch", "nazwa" : "sztab", "rotacja" : 1, "rany" : 0}])
        # print(correct_output)
        assert(Diff().compare(output, correct_output))
        # assert(output == correct_output)
    
test = Tests()
test.test_bitwa1()