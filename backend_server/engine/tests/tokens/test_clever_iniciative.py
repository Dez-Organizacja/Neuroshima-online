from main.tokens.Clever_iniciative import CleverIniciative

def assert_activates(initiative, value):
    assert initiative.activate(value) is False

def assert_does_not_activate(initiative, value):
    assert initiative.activate(value) is True

class TestCleverIniciative:
    def test_CI1(self):
        initiative = CleverIniciative([2, 1])

        assert_activates(initiative, 2)
        assert_does_not_activate(initiative, 2)

        assert_activates(initiative, 1)
        assert_does_not_activate(initiative, 1)

    def test_CI2(self):
        initiative = CleverIniciative([2, 1])
        initiative.iniciative_boosts = 1

        assert_activates(initiative, 3)
        assert_activates(initiative, 2)
        assert_does_not_activate(initiative, 1)

    def test_CI3(self):
        initiative = CleverIniciative([0])
        initiative.num_of_new = 1
        initiative.end_booster_faze()
        initiative.iniciative_boosts = 1

        assert initiative.INICIATIVE == [0, -1]
        assert_activates(initiative, 1)
        assert_activates(initiative, 0)
        assert_does_not_activate(initiative, -1)

    def test_CI4(self):
        initiative = CleverIniciative([3, 1])
        initiative.iniciative_boosts = 2
        initiative.is_blocked_to_0 = True

        assert_does_not_activate(initiative, 3)
        assert_does_not_activate(initiative, 1)
        assert_activates(initiative, 0)


    def test_CI5(self):
        initiative = CleverIniciative([2])
        initiative.num_of_new = 1
        initiative.end_booster_faze()

        assert initiative.INICIATIVE == [2, 1]
        assert_activates(initiative, 2)
        assert_does_not_activate(initiative, 2)

        initiative.begin_iniciative()

        assert initiative.INICIATIVE == [2]
        assert_activates(initiative, 2)
