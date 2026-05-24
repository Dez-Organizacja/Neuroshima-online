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
        return self.tokens[place]

    def import_token(self, name):
        self.draw_token(TokenFactory().create(name, self.fraction))


    def load_list(self, data : list[str]):
        self.tokens = []
        for token in data:
            self.import_token(token)

    def to_list(self) -> list[str]:
        data = []
        for token in self.tokens:
            data.append(token.name)
        return data
    
    def print_hand(self):
        print(self.to_list())