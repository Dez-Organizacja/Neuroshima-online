from main.tokens.clever_initiative import CleverInitiative

def assert_activates(initiative, value):
    assert initiative.activate(value) is True

def assert_does_not_activate(initiative, value):
    assert initiative.activate(value) is False

class TestCleverInitiative:
    def test_CI1(self):
        initiative = CleverInitiative([2, 1])

        assert_activates(initiative, 2)
        assert_does_not_activate(initiative, 2)

        assert_activates(initiative, 1)
        assert_does_not_activate(initiative, 1)

    def test_CI2(self):
        initiative = CleverInitiative([2, 1])
        initiative.initiative_boosts = 1

        assert_activates(initiative, 3)
        assert_activates(initiative, 2)
        assert_does_not_activate(initiative, 1)

    def test_CI3(self):
        initiative = CleverInitiative([0])
        initiative.num_of_new = 1
        initiative.end_booster_faze()
        initiative.initiative_boosts = 1

        assert initiative.initiative == [0, -1]
        assert_activates(initiative, 1)
        assert_activates(initiative, 0)
        assert_does_not_activate(initiative, -1)

    def test_CI4(self):
        initiative = CleverInitiative([3, 1])
        initiative.initiative_boosts = 2
        initiative.is_blocked_to_0 = True

        assert_does_not_activate(initiative, 3)
        assert_does_not_activate(initiative, 1)
        assert_activates(initiative, 0)


    def test_CI5(self):
        initiative = CleverInitiative([2])
        initiative.num_of_new = 1
        initiative.end_booster_faze()

        assert initiative.initiative == [2, 1]
        assert_activates(initiative, 2)
        assert_does_not_activate(initiative, 2)

        initiative.begin_initiative()

        assert initiative.initiative == [2]
        assert_does_not_activate(initiative, 2)

    def test_import_export_preserves_used_and_basic_initiatives(self):
        initiative = CleverInitiative([2])
        initiative.num_of_new = 1
        initiative.end_booster_faze()

        assert initiative.to_dict() == {
            "initiative": [2, 1],
            "is_used": [False, False],
            "is_basic": [True, False],
            "num_of_old": 1,
        }

        assert_activates(initiative, 2)

        restored = CleverInitiative([])
        restored.from_dict(initiative.to_dict())

        assert restored.to_dict() == initiative.to_dict()
        assert_does_not_activate(restored, 2)
        assert_activates(restored, 1)

        restored.begin_initiative()

        assert restored.to_dict() == {
            "initiative": [2],
            "is_used": [True, True],
            "is_basic": [True, False],
            "num_of_old": 0,
        }

    def test_import_export_preserves_battle_modifiers(self):
        initiative = CleverInitiative([3, 1])
        initiative.initiative_boosts = 2
        initiative.is_blocked_to_0 = True

        restored = CleverInitiative([])
        restored.from_dict(initiative.to_dict())

        assert restored.initiative_boosts == 0
        assert restored.is_blocked_to_0 is False
        assert_activates(restored, 3)
        assert_does_not_activate(restored, 0)
