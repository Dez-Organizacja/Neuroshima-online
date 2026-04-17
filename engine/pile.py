from random import shuffle
import wszystkie_frakcje
from variable import *

class Pile():
    def __init__(self, fraction):
        self.tokens = []
        self.fraction = fraction

    def add_token(self, name):
        self.tokens.append(name)

    def remove_token(self, name):
        for i in range(len(self.tokens)):
            if(name == self.tokens[i]):
                self.tokens.pop(i)
                return

    def new_pile(self):
        self.tokens = []
        for name, data in wszystkie_frakcje.frakcje.get(self.fraction, {}).items():
            for _ in range(data[Token.UNIT_COUNT]):
                self.add_token(name)
        shuffle(self.tokens)

    def from_list(self, data):
        self.tokens = []
        for name in data:
            self.add_token(name)

    def to_list(self):
        data = []
        for token in self.tokens:
            data.append(token)
        return data
    
    def print_pile(self):
        print(self.to_list())

    def draw_token(self):
        return self.tokens.pop()
    
    def is_empty(self):
        return len(self.tokens) == 0