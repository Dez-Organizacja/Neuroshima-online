import pytest
from akcje import Actions

class DummyGame:
    def __init__(self):
        self.bottoms = {"xd"}

class Test_hand:
    def test_resize_hand(self):
        game = DummyGame()
        actions = Actions(game)
        hand = ["a", "b", None, None]
        actions.resize_hand(hand)
        assert hand == ["a", "b"]

    def test_fill_hand(self):
        game = DummyGame()
        actions = Actions(game)
        hand = ["a"]
        actions.fill_hand(hand)
        assert len(hand) == 3
        assert hand[1] is None
        assert hand[2] is None

    def test_dobierz(self):
        game = DummyGame()
        actions = Actions(game)
        hand = ["a"]
        pile = ["b", "c"]
        actions.dobierz(hand, pile, "b")
        assert hand == ["a", "b"]
        assert pile == ["c"]

    def test_odrzuc(self):
        game = DummyGame()
        actions = Actions(game)
        hand = ["a", "b"]
        actions.odrzuc(hand, "a")
        assert hand == ["b"]
