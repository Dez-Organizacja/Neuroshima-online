import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from akcje import Actions
from hand import Hand
from pile import Pile
from variable import *
# class DummyGame:
#     MAX_HAND_SIZE = 3
#     def __init__(self):
#         self.bottoms = {"xd"}

class Test_hand:
    # def test_resize_hand(self):
    #     game = DummyGame()
    #     actions = Actions(game)
    #     hand = ["a", "b", None, None]
    #     actions.resize_hand(hand)
    #     assert hand == ["a", "b"]

    # def test_fill_hand(self):
    #     game = DummyGame()
    #     actions = Actions(game)
    #     hand = ["a"]
    #     actions.fill_hand(hand)
    #     assert len(hand) == 3
    #     assert hand[1] is None
    #     assert hand[2] is None

    def test_draw_tokens(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz"]})
        pile = Pile("moloch")
        pile.from_list(["ruch", "klaun", "bloker"])
        hand.draw_tokens(pile, "normal")

        assert hand.tokens == ["sieciarz", "bloker", "klaun"]
        assert pile.tokens == ["ruch"]

    def test_draw_tokens2(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz"]})
        pile = Pile("moloch")
        pile.from_list(["ruch", "klaun", "bloker"])
        hand.draw_tokens(pile, Turn.Type.SECOND)

        assert hand.tokens == ["sieciarz", "bloker"]
        assert pile.tokens == ["ruch", "klaun"]

    def test_get_token(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz", "bloker", "klaun"]})
        token = hand.get_token(1)
        assert(token == "bloker")
        assert(hand.active_token == 1)

        token = hand.get_active_token()
        assert(token == "bloker")
        assert(hand.active_token == 1)

    def test_discard_last(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz", "bloker", "klaun"]})
        hand.get_token(1)
        hand.discard_last()
        assert (hand.tokens == ["sieciarz", "klaun"])
        assert (hand.active_token == None)

    # def test_odrzuc(self):
    #     game = DummyGame()
    #     actions = Actions(game)
    #     hand = ["a", "b"]
    #     actions.odrzuc(hand, "a")
    #     assert hand == ["b"]
