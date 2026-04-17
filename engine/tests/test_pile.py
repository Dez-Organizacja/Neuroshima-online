import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pile import Pile


class Test_Pile:
    
    def test_remove_token(self):
        pile = Pile("moloch")
        pile.from_list(["klaun", "ruch", "sztab"])
        pile.remove_token("klaun")
        assert(pile.tokens == ["ruch", "sztab"])