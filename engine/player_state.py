from hand import Hand
from pile import Pile

class PlayerState:
    HAND_KEY = "hand"
    PILE_KEY = "pile"

    def __init__(self, fraction):
        self.fraction = fraction
        self.hand = Hand(fraction)
        self.pile = Pile(fraction)
    
    @classmethod
    def from_dict(cls, fraction, data):
        obj = cls(fraction)
        obj.hand.from_dict(data.get(cls.HAND_KEY, {}))
        obj.pile.from_list(data.get(cls.PILE_KEY, []))
        return obj

    def to_dict(self):
        data = {
            self.HAND_KEY : self.hand.to_dict(),
            self.PILE_KEY : self.pile.to_list()
        }
        return data
    
    def print_state(self):
        print(self.to_dict())

    def new_game(self):
        self.pile.new_pile()
