from main.utils.variable import *
from main.tokens.abstract_token import Token
from main.tokens.data import Ability, TokenType

class InstantToken(Token):
    def __init__(self, name, fraction):
        super().__init__(
            name=name,
            fraction=fraction,
            type=TokenType.INSTANT,
            ability=Ability(name)
        )