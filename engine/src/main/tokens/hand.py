from main.tokens.token_factory import TokenFactory
from main.tokens.abstract_token import Token

class Hand():
    TOKENS_KEY = "tokens"

    def __init__(self, fraction):
        self.tokens = []
        self.fraction = fraction

    def discard_token(self, slot):
        self.tokens.pop(slot)

    @property
    def size(self):
        return len(self.tokens)

    def draw_token(self, token : Token):
        self.tokens.append(token)

    def get_token(self, place) -> Token:
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

    def to_dict(self) -> list[str]:
        tokens = []
        for token in self.tokens:
            tokens.append(token.name)
        data = {self.ACTIVE_TOKEN_KEY : self.active_token, self.TOKENS_KEY : tokens}
        return data
    
    def print_hand(self):
        print(self.to_list())