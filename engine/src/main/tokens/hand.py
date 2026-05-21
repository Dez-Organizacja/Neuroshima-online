from main.utils.variable import Turn
from main.tokens.data import BoardType
from main.tokens.token_factory import TokenFactory
from main.tokens.abstract_token import Token

class Hand():
    HAND_LIMITS = {
        Turn.Type.FIRST : 1,
        Turn.Type.HQ_PLACEMENT : 1,
        Turn.Type.SECOND : 2
    }
    DEFAULT_HAND_LIMIT = 3
    TOKENS_KEY = "tokens"

    def __init__(self, fraction):
        self.tokens = []
        self.fraction = fraction

    def discard_token(self, slot):
        self.tokens.pop(slot)

    @property
    def size(self):
        return len(self.tokens)
    
    def get_hand_limit(self, turn_type):
        return self.HAND_LIMITS.get(turn_type, self.DEFAULT_HAND_LIMIT)

    def is_full(self, turn_type):
        return self.size >= self.get_hand_limit(turn_type)

    def draw_token(self, token):
        self.tokens.append(token)

    def draw_tokens(self, pile, turn_type):
        if(turn_type == Turn.Type.HQ_PLACEMENT):
            drawn_token = pile.remove_token(BoardType.HQ)
            self.draw_token(drawn_token)
            return

        while(not self.is_full(turn_type) and not pile.is_empty()):
            drawn_token = pile.remove_token()
            self.tokens.append(drawn_token)

    def get_token(self, place):
        if(place < 0 or place >= len(self.tokens)):
            return None
        self.active_token = place
        return self.tokens[place]

    def import_token(self, name):
        self.draw_token(TokenFactory().create(name, self.fraction))

    def from_dict(self, data):
        self.tokens = []
        self.active_token = data.get(self.ACTIVE_TOKEN_KEY, None)
        for token in data.get(self.TOKENS_KEY, []):
            self.import_token(token)

    def to_dict(self):
        tokens = []
        for token in self.tokens:
            tokens.append(token.export())
        data = {self.ACTIVE_TOKEN_KEY : self.active_token, self.TOKENS_KEY : tokens}
        return data
    
    def print_hand(self):
        print(self.to_list())