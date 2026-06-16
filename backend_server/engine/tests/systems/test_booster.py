from main.board.board import Board
from main.systems.boosters import BoosterSolver
from main.attacks.config import AttackType
from main.rules.combat import CombatRules

def solve_boosters(board: Board) -> None:
    BoosterSolver(board)    


def place(
    board: Board,
    pos: tuple[int, int],
    name: str,
    faction: str,
    rotation: int = 0,
    wired: bool = False,
):
    board.put_token(pos, name, faction)
    token = board.get_token(pos)
    token.set_rotation(rotation)
    if wired:
        token.set_wire()
    return token


def token_at(board: Board, pos: tuple[int, int]):
    return board.get_token(pos)


def melee_boosts(board: Board, pos: tuple[int, int]) -> int:
    return token_at(board, pos).get_attack_boost(AttackType.MELEE)


def initiatives(board: Board, pos: tuple[int, int]) -> list[int]:
    return token_at(board, pos).state.modifiers.initiatives


def initiative_boosts(board: Board, pos: tuple[int, int]) -> int:
    return token_at(board, pos).state.modifiers.initiative_boosts


class TestBoosters:
    def test_melee_boost_targets_own_units_only(self):
        board = Board()
        place(board, (2, 4), "oficer", "borgo")
        place(board, (1, 5), "mutek", "borgo")
        place(board, (1, 3), "mutek", "borgo")
        place(board, (2, 6), "lowca", "moloch")

        solve_boosters(board)

        assert melee_boosts(board, (1, 5)) == 1
        assert melee_boosts(board, (1, 3)) == 1
        assert melee_boosts(board, (2, 6)) == 0

    def test_melee_boosts_stack_from_multiple_sources(self):
        board = Board()
        place(board, (2, 4), "mutek", "borgo")
        place(board, (3, 3), "oficer", "borgo")
        place(board, (2, 2), "oficer", "borgo")

        solve_boosters(board)

        assert melee_boosts(board, (2, 4)) == 2

    def test_melee_boosts_are_recomputed_after_source_is_removed(self):
        board = Board()
        place(board, (2, 4), "mutek", "borgo")
        place(board, (3, 3), "oficer", "borgo")
        place(board, (2, 2), "oficer", "borgo")

        solve_boosters(board)
        board.destroy_token((3, 3))
        solve_boosters(board)

        assert melee_boosts(board, (2, 4)) == 1

    def test_wired_booster_does_not_emit_boosts(self):
        board = Board()
        place(board, (2, 4), "oficer", "borgo", wired=True)
        place(board, (1, 5), "mutek", "borgo")

        solve_boosters(board)

        assert melee_boosts(board, (1, 5)) == 0

    def test_boost_directions_follow_rotation(self):
        board = Board()
        place(board, (2, 4), "oficer", "borgo", rotation=2)
        place(board, (3, 5), "mutek", "borgo")
        place(board, (1, 5), "mutek", "borgo")

        solve_boosters(board)

        assert melee_boosts(board, (3, 5)) == 1
        assert melee_boosts(board, (1, 5)) == 0

    def test_new_initiative_adds_next_lower_initiative(self):
        board = Board()
        place(board, (2, 4), "matka", "moloch")
        place(board, (1, 5), "klaun", "moloch")

        solve_boosters(board)

        assert initiatives(board, (1, 5)) == [2, 1]

    def test_new_initiatives_stack_without_duplicates(self):
        board = Board()
        place(board, (2, 4), "klaun", "moloch")
        place(board, (3, 3), "matka", "moloch")
        place(board, (2, 6), "matka", "moloch", rotation=4)
        place(board, (1, 3), "matka", "moloch", rotation=2)

        solve_boosters(board)

        assert initiatives(board, (2, 4)) == [2, 1, 0, -1]

    def test_new_initiative_does_not_affect_units_without_base_initiative(self):
        board = Board()
        place(board, (2, 4), "matka", "moloch")
        place(board, (1, 5), "sieciarz", "moloch")

        solve_boosters(board)

        assert initiatives(board, (1, 5)) == []

    def test_initiative_boost_changes_activation_level(self):
        board = Board()
        place(board, (2, 4), "zwiadowca", "borgo")
        target = place(board, (1, 5), "mutek", "borgo")

        solve_boosters(board)

        assert initiative_boosts(board, (1, 5)) == 1
        assert CombatRules.can_activate(target, 3) is True
        assert CombatRules.can_activate(target, 2) is False

    def test_minus_initiative_targets_enemies_only(self):
        board = Board()
        enemy = place(board, (1, 5), "lowca", "moloch")
        own = place(board, (2, 6), "komandos", "posterunek")
        place(board, (2, 4), "dywersant", "posterunek")

        solve_boosters(board)

        assert enemy.state.modifiers.initiative_boosts == -1
        assert own.state.modifiers.initiative_boosts == 0
        assert CombatRules.can_activate(enemy, 2) is True
        assert CombatRules.can_activate(enemy, 3) is False

    def test_steal_boost_makes_enemy_booster_target_enemies(self):
        board = Board()
        place(board, (2, 4), "skoper", "posterunek")
        place(board, (1, 5), "mozg", "moloch")
        place(board, (2, 6), "silacz", "posterunek")
        place(board, (1, 3), "lowca", "moloch")

        solve_boosters(board)

        assert melee_boosts(board, (2, 6)) == 1
        assert melee_boosts(board, (1, 3)) == 0

    def test_stolen_boost_target_resets_after_stealer_is_removed(self):
        board = Board()
        place(board, (2, 4), "skoper", "posterunek")
        place(board, (1, 5), "mozg", "moloch")
        place(board, (2, 6), "silacz", "posterunek")
        place(board, (1, 3), "lowca", "moloch")

        solve_boosters(board)
        board.destroy_token((2, 4))
        solve_boosters(board)

        assert melee_boosts(board, (2, 6)) == 0
        assert melee_boosts(board, (1, 3)) == 1

    # def test_board_healing_maps_are_refreshed_after_boosters(self):
    #     board = Board()
    #     place(board, (2, 4), "medyk", "moloch")
    #     target = place(board, (1, 5), "sztab", "moloch")
    #     target.add_wounds(1)

    #     solve_boosters(board)

    #     assert board.my_targets == {(2, 4): [(1, 5)]}
    #     assert board.my_healers == {(1, 5): [(2, 4)]}

    # def test_board_healing_maps_use_stolen_heal_target_relation(self):
    #     board = Board()
    #     place(board, (2, 2), "skoper", "posterunek")
    #     place(board, (2, 4), "medyk", "moloch")
    #     ally = place(board, (1, 5), "sztab", "moloch")
    #     enemy = place(board, (3, 5), "silacz", "posterunek")
    #     ally.add_wounds(1)
    #     enemy.add_wounds(1)

    #     solve_boosters(board)

        # assert board.my_targets == {(2, 4): [(3, 5)]}
        # assert board.my_healers == {(3, 5): [(2, 4)]}

    # def test_board_healing_maps_are_cleared_when_target_is_removed(self):
    #     board = Board()
    #     place(board, (2, 4), "medyk", "moloch")
    #     target = place(board, (1, 5), "sztab", "moloch")
    #     target.add_wounds(1)

    #     solve_boosters(board)
    #     board.destroy_token((1, 5))
    #     solve_boosters(board)

    #     assert board.my_targets == {}
    #     assert board.my_healers == {}

    # def test_board_healing_maps_collect_multiple_healers_for_same_target(self):
    #     board = Board()
    #     target = place(board, (2, 4), "sztab", "moloch")
    #     target.add_wounds(1)
    #     place(board, (1, 3), "medyk", "moloch")
    #     place(board, (2, 6), "medyk", "moloch")
    #     place(board, (3, 3), "medyk", "moloch")

    #     solve_boosters(board)

    #     assert board.my_targets == {
    #         (1, 3): [(2, 4)],
    #         (2, 6): [(2, 4)],
    #         (3, 3): [(2, 4)],
    #     }
    #     assert set(board.my_healers[(2, 4)]) == {(1, 3), (2, 6), (3, 3)}
    #     assert len(board.my_healers) == 1

    # def test_board_healing_maps_skip_wired_healers(self):
    #     board = Board()
    #     place(board, (2, 4), "medyk", "moloch", wired=True)
    #     target = place(board, (1, 5), "sztab", "moloch")
    #     target.add_wounds(1)

    #     solve_boosters(board)

    #     assert board.my_targets == {}
    #     assert board.my_healers == {}
