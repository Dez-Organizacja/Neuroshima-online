from zeton import Zeton
from instant_token import InstantToken
import wszystkie_frakcje
from variable import *
from abc import ABC, abstractmethod

class TokenFactory():
    @staticmethod
    def create(name, fraction, data):
        stats = wszystkie_frakcje.frakcje.get(fraction, {}).get(name, None)
        token_type = stats.get(TokenKey.TYPE)
        if(token_type == TokenType.INSTANT):
            return InstantToken(name, fraction)
        elif(token_type == TokenType.BOARD):
            return Zeton(data)


class Token(ABC):

    def __init__(self, fraction, name):
        self.fraction = fraction
        self.name = name