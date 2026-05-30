import pytest

from main.board.board import Board
from main.systems.boosters import BoosterSolver
from main.tokens.Clever_iniciative import CleverIniciative

def solve_boosters(board):
    BoosterSolver(board)

def initiatives(board, pos):
    return board.get_token(pos).clever_iniciative.iniciative

def activates_at(board, pos, initiative, can = False):
    return can == board.get_token(pos).clever_iniciative.activate(initiative)

def can_activates_at(board, pos, initiative, can):
    return can == board.get_token(pos).clever_iniciative.can_activate(initiative)

class TestBoost:
    def test_boost1(self):
        # moloch -> molocha i borgo + rekalkulacja
        board = Board()

        board.import_token((2, 4), {"name": "oficer", "faction": "moloch", "rotation": 1})
        board.import_token((2, 6), {"name": "hybryda", "faction": "moloch", "rotation": 0})
        board.import_token((3, 5), {"name": "obronca", "faction": "moloch", "rotation": 0})
        board.import_token((2, 2), {"name": "mutek", "faction": "borgo", "rotation": 0})
        board.import_token((1, 5), {"name": "szturmowiec", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert board.get_token((2, 6)).shoot_boosts == 0
        assert board.get_token((3, 5)).shoot_boosts == 1
        assert board.get_token((2, 2)).shoot_boosts == 0
        assert board.get_token((1, 5)).shoot_boosts == 1

        solve_boosters(board)

        assert board.get_token((2, 6)).shoot_boosts == 0
        assert board.get_token((3, 5)).shoot_boosts == 1
        assert board.get_token((2, 2)).shoot_boosts == 0
        assert board.get_token((1, 5)).shoot_boosts == 1


    def test_boost2(self):
        # kilka naraz
        board = Board()

        board.import_token((2, 4), {"name": "juggernaut", "faction": "moloch", "rotation": 0})
        board.import_token((2, 2), {"name": "oficer", "faction": "moloch", "rotation": 0})
        board.import_token((1, 3), {"name": "mozg", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        target = board.get_token((2, 4))
        assert target.shoot_boosts == 2
        assert target.meele_boosts == 1


    def test_boost3(self):
        # basic inicjative
        board = Board()

        board.import_token((2, 4), {"name": "zwiadowca", "faction": "borgo", "rotation": 0})
        board.import_token((1, 5), {"name": "mutek", "faction": "borgo", "rotation": 0})
        board.import_token((2, 6), {"name": "nozownik", "faction": "borgo", "rotation": 0})
        board.import_token((1, 3), {"name": "hybryda", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert board.get_token((1, 5)).clever_iniciative.iniciative_boosts == 1
        assert board.get_token((2, 6)).clever_iniciative.iniciative_boosts == 1
        assert board.get_token((1, 3)).clever_iniciative.iniciative_boosts == 0


    def test_boost4(self):
        # matka test 1
        board = Board()

        board.import_token((2, 4), {"name": "klaun", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [2, 1]


    def test_boost5_stack(self):
        # duzo matek
        board = Board()

        board.import_token((2, 4), {"name": "klaun", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})
        board.import_token((2, 6), {"name": "matka", "faction": "moloch", "rotation": 4})
        board.import_token((3, 5), {"name": "matka", "faction": "moloch", "rotation": 5})

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [2, 1, 0, -1]


    # def test_new_initiative_modules_stack_from_three_to_three_two_one():
    #     board = Board()

    #     board.import_token((2, 4), {"name": "hybryda", "faction": "moloch", "rotation": 0})
    #     board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})
    #     board.import_token((2, 6), {"name": "matka", "faction": "moloch", "rotation": 4})

    #     solve_boosters(board)

    #     assert initiatives(board, (2, 4)) == [3, 2, 1]

    def test_boost5(self):
        # duzo matek
        board = Board()

        board.import_token((2, 4), {"name": "klaun", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})
        board.get_token((2, 4)).clever_iniciative = CleverIniciative([3, 1])

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [3, 2, 1]
        

    def test_boost6(self):
        # matka + mniej niz zero
        board = Board()

        board.import_token((2, 4), {"name": "sztab", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [0, -1]


    def test_boost7(self):
        # bez inicjatywy
        board = Board()

        board.import_token((2, 4), {"name": "sieciarz", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == []


    def test_boost8(self):
        # test aktywacji
        board = Board()

        board.import_token((2, 4), {"name": "klaun", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})
        board.import_token((1, 3), {"name": "zwiadowca", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [2, 1]
        assert board.get_token((2, 4)).clever_iniciative.iniciative_boosts == 1
        assert activates_at(board, (2, 4), 3)
        assert activates_at(board, (2, 4), 2)
        assert not activates_at(board, (2, 4), 1)


    def test_boost9(self):
        # czy dziala z ujemnym
        board = Board()

        board.import_token((2, 4), {"name": "sztab", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})
        board.import_token((1, 3), {"name": "zwiadowca", "faction": "moloch", "rotation": 0})

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [0, -1]
        assert board.get_token((2, 4)).clever_iniciative.iniciative_boosts == 1

        solve_boosters(board)

        assert board.get_token((2, 4)).clever_iniciative.iniciative_boosts == 1
        assert activates_at(board, (2, 4), 1)
        assert activates_at(board, (2, 4), 0)
        assert not activates_at(board, (2, 4), -1)


    def test_boost10(self):
        # czy dziala rekalkulacja
        board = Board()

        board.import_token((2, 4), {"name": "klaun", "faction": "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})

        solve_boosters(board)
        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [2, 1]

    def test_boost11(self):
        board = Board()

        board.import_token((2, 4), {"name": "opancerzonylowca", "faction" : "moloch", "rotation": 0})
        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})

        solve_boosters(board)
        solve_boosters(board)

        assert can_activates_at(board, (2, 4), 3, True)
        assert can_activates_at(board, (2, 4), 2, False)
        assert can_activates_at(board, (2, 4), 1, False)

        assert activates_at(board, (2, 4), 2)

        board.import_token((2, 2), {"name": "matka", "faction": "moloch", "rotation": 1})

        solve_boosters(board)

        assert can_activates_at(board, (2, 4), 3, True)
        assert can_activates_at(board, (2, 4), 2, False)
        assert can_activates_at(board, (2, 4), 1, False)
        assert can_activates_at(board, (2, 4), 0, False)

        board.destroy_token((3, 3))
        solve_boosters(board)

        assert can_activates_at(board, (2, 4), 3, True)
        assert can_activates_at(board, (2, 4), 2, False)
        assert can_activates_at(board, (2, 4), 1, False)
        assert can_activates_at(board, (2, 4), 0, True)

        assert activates_at(board, (2, 4), 2)
        assert activates_at(board, (2, 4), 1)

        board.import_token((3, 3), {"name": "matka", "faction": "moloch", "rotation": 0})
        board.import_token((1, 3), {"name": "matka", "faction": "moloch", "rotation": 2})

        solve_boosters(board)

        assert can_activates_at(board, (2, 4), 3, True)
        assert can_activates_at(board, (2, 4), 2, False)
        assert can_activates_at(board, (2, 4), 1, False)
        assert can_activates_at(board, (2, 4), 0, False)

    # def test_boost12():
    #     board = Board()
