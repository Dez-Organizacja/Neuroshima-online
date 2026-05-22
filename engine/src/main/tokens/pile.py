from random import shuffle
import main.frakcje.wszystkie_frakcje as allfraction
from main.tokens.data import TokenKey
from main.tokens.abstract_token import Token
from main.tokens.token_factory import TokenFactory

class Pile():
    def __init__(self, fraction):
        self.tokens : list[Token] = []
        self.fraction = fraction

    def add_token(self, name):
        self.tokens.append(TokenFactory().create(name, self.fraction))

    def remove_token(self, name=None) -> Token:
        if name:
            for i in range(len(self.tokens)):
                if(name == self.tokens[i].name):
                    return self.tokens.pop(i)
        return self.tokens.pop()

    def new_pile(self):
        self.tokens = []
        for name, data in allfraction.frakcje.get(self.fraction, {}).items():
            for _ in range(data[TokenKey.UNIT_COUNT]):
                self.add_token(name)
        shuffle(self.tokens)

    def from_list(self, data):
        self.tokens = []
        for name in data:
            self.add_token(name)

    def to_list(self) -> list[str]:
        data = []
        for token in self.tokens:
            # print(token.name)
            data.append(token.name)
        return data
    
    def print_pile(self):
        print(self.to_list())

    def get_token(self) -> Token:
        return self.tokens.pop()
    
    @property
    def empty(self):
        return len(self.tokens) == 0