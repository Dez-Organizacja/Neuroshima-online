from types import SimpleNamespace

from main.tokens.clever_initiative import CleverInitiative


def make_token(initiative):
    modifiers = SimpleNamespace(
        initiatives=[],
        is_used=[],
        is_basic=[],
        num_of_old=0,
        is_blocked_to_0=False,
        initiative_boosts=0,
        num_of_new=0,
    )
    return SimpleNamespace(
        config=SimpleNamespace(initiative=list(initiative)),
        state=SimpleNamespace(modifiers=modifiers),
    )


def assert_activates(token, value):
    assert CleverInitiative.activate(token, value) is True


def assert_does_not_activate(token, value):
    assert CleverInitiative.activate(token, value) is False


class TestCleverInitiative:
    def test_add_and_remove_initiative(self):
        token = make_token([2, 1])
        CleverInitiative.begin_initiative(token)

        CleverInitiative.add_initiative(token)
        assert token.state.modifiers.initiatives == [2, 1, 0]
        assert token.state.modifiers.is_used == [False, False, False]
        assert token.state.modifiers.is_basic == [True, True, False]

        CleverInitiative.remove_initiative(token)
        assert token.state.modifiers.initiatives == [2, 1]
        assert token.state.modifiers.is_used == [False, False]
        assert token.state.modifiers.is_basic == [True, True]

    def test_activation_respects_boosts(self):
        token = make_token([2, 1])
        CleverInitiative.begin_initiative(token)
        token.state.modifiers.initiative_boosts = 1

        assert CleverInitiative.can_activate(token, 3) is True
        assert CleverInitiative.can_activate(token, 2) is True
        assert CleverInitiative.can_activate(token, 1) is False

        assert_activates(token, 3)
        assert_activates(token, 2)
        assert_does_not_activate(token, 2)

    def test_zero_initiative_and_blocking(self):
        token = make_token([0])
        CleverInitiative.begin_initiative(token)
        token.state.modifiers.num_of_new = 1
        CleverInitiative.end_booster_faze(token)
        token.state.modifiers.initiative_boosts = 1

        assert token.state.modifiers.initiatives == [0, -1]
        assert CleverInitiative.can_activate(token, 1) is True
        assert CleverInitiative.can_activate(token, 0) is True
        assert_does_not_activate(token, -1)

        assert_activates(token, 1)
        assert_activates(token, 0)
        assert_does_not_activate(token, 0)

        token = make_token([3, 1])
        CleverInitiative.begin_initiative(token)
        token.state.modifiers.initiative_boosts = 2
        token.state.modifiers.is_blocked_to_0 = True

        assert CleverInitiative.can_activate(token, 3) is False
        assert CleverInitiative.can_activate(token, 1) is False
        assert CleverInitiative.can_activate(token, 0) is False
        assert_does_not_activate(token, 3)
        assert_does_not_activate(token, 1)
        assert_does_not_activate(token, 0)

    def test_begin_initiative_resets_state(self):
        token = make_token([2])
        CleverInitiative.begin_initiative(token)
        token.state.modifiers.num_of_new = 1
        CleverInitiative.end_booster_faze(token)
        token.state.modifiers.initiative_boosts = 2
        token.state.modifiers.is_blocked_to_0 = True
        CleverInitiative.activate(token, 2)

        CleverInitiative.begin_initiative(token)

        assert token.state.modifiers.initiatives == [2]
        assert token.state.modifiers.is_used == [False]
        assert token.state.modifiers.is_basic == [True]
        assert token.state.modifiers.num_of_old == 0
        assert token.state.modifiers.is_blocked_to_0 is False
        assert token.state.modifiers.initiative_boosts == 0
        assert token.state.modifiers.num_of_new == 0

    def test_import_export_roundtrip(self):
        token = make_token([2])
        CleverInitiative.begin_initiative(token)
        token.state.modifiers.num_of_new = 1
        CleverInitiative.end_booster_faze(token)
        token.state.modifiers.initiative_boosts = 1
        CleverInitiative.activate(token, 3)
        token.state.modifiers.is_blocked_to_0 = True

        data = CleverInitiative.to_dict(token)
        assert data == {
            "initiative": [2, 1],
            "is_used": [True, False],
            "is_basic": [True, False],
            "num_of_old": 1,
            "is_blocked_to_0": True,
            "initiative_boosts": 1,
            "num_of_new": 1,
        }

        restored = make_token([])
        CleverInitiative.from_dict(restored, data)
        assert CleverInitiative.to_dict(restored) == data

        assert CleverInitiative.can_activate(restored, 3) is False
        assert CleverInitiative.can_activate(restored, 2) is False
        assert CleverInitiative.can_activate(restored, 1) is False
