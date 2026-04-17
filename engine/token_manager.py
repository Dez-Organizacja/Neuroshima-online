from hand import Hand
from pile import Pile
from variable import Turn

class TokenManager:
    CURRENT_FRACTION_KEY = "current_fraction"
    NAME_KEY = "token_manager"
    HAND_KEY = "hand"
    PILE_KEY = "pile"
    def __init__(self, fractions):
        self.fractions = fractions
        self.hand = Hand()
        self.pile = Pile()
        self.current_fraction = None
        self.turn_type = None

    def import_tokens(self, data):
        self.current_fraction = data.get(TokenManager.CURRENT_FRACTION_KEY, None)
        self.turn_type = data.get(Turn.TYPE, None)
        token_data = data.get(self.NAME_KEY, None)
        self.hand.from_dict(token_data.get(self.HAND_KEY, {}))
        self.pile.from_dict(token_data.get(self.PILE_KEY, {}))

    def export_tokens(self):
        return {
            self.HAND_KEY : self.hand.to_dict(),
            self.PILE_KEY : self.pile.to_dict()
        }
    
    def set_current_fraction(self, fraction):
        if(fraction in self.fractions):
            self.current_fraction = fraction
        else:
            self.current_fraction = None
    
    def new_turn(self, fraction, turn_type):
        self.set_current_fraction(fraction)
        self.turn_type = turn_type
        self.draw_tokens()

    def draw_tokens(self):
        if(self.current_fraction is None):
            return False
        
        self.hand.draw_tokens()