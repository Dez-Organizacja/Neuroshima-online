from main.tokens.board_token import BoardToken
from main.tokens.instant_token import InstantToken
from main.tokens.data import TokenKey, TokenType
import main.frakcje.wszystkie_frakcje as allfractions

class TokenFactory():
    @staticmethod
    def create(name, fraction, data={}):
        stats = allfractions.frakcje.get(fraction, {}).get(name, {})
        token_type = stats.get(TokenKey.TYPE)
        if(token_type == TokenType.INSTANT):
            return InstantToken(name, fraction)
        elif(token_type == TokenType.BOARD):
            return BoardToken(name, fraction, data)
        raise ValueError(f"nie znaleziono żetonu o nazwie {name} z frakcji {fraction}")