from variable import *

class Hand():
    HAND_LIMITS = {
        Turn.Type.FIRST : 1,
        Turn.Type.SECOND : 2
    }
    DEFAULT_HAND_LIMIT = 3
    ACTIVE_TOKEN_KEY = "active_token"
    TOKENS_KEY = "tokens"

    def __init__(self, fraction):
        self.tokens = []
        self.fraction = fraction
        self.active_token = None

    def add_token(self, token):
        self.tokens.append(token)

    def discard_last(self):
        self.tokens.pop(self.active_token)
        self.active_token = None

    def get_hand_limit(self, turn_type):
        return self.HAND_LIMITS.get(turn_type, self.DEFAULT_HAND_LIMIT)

    def draw_tokens(self, pile, turn_type):
        if(turn_type == Turn.Type.HQ_PLACEMENT):
            drawn_token = Token.Type.Board.HQ
            pile.remove_token(drawn_token)
            self.add_token(drawn_token)
            return

        while(len(self.tokens) < self.get_hand_limit(turn_type) and not pile.is_empty()):
            drawn_token = pile.draw_token()
            self.tokens.append(drawn_token)

    def get_token(self, place):
        if(place < 0 or place >= len(self.tokens)):
            return None
        self.active_token = place
        return self.tokens[place]

    def get_active_token(self):
        if(self.active_token is None):
            return None
        return self.get_token(self.active_token)

    def from_dict(self, data):
        self.tokens = []
        self.active_token = data.get(self.ACTIVE_TOKEN_KEY, None)
        for token in data.get(self.TOKENS_KEY, []):
            self.add_token(token)

    def to_dict(self):
        tokens = []
        for token in self.tokens:
            tokens.append(token)
        data = {self.ACTIVE_TOKEN_KEY : self.active_token, self.TOKENS_KEY : tokens}
        return data
    
    def print_hand(self):
        print(self.to_list())