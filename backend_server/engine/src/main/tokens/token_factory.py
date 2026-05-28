from main.tokens.board_token import BoardToken
from main.tokens.instant_token import InstantToken
from main.tokens.data import TokenKey, TokenType
import main.frakcje.wszystkie_frakcje as allfractions

class TokenFactory():
    @staticmethod
    def create(name, faction, data={}):
        stats = allfractions.frakcje.get(faction, {}).get(name, {})
        token_type = stats.get(TokenKey.TYPE)
        if(token_type == TokenType.INSTANT):
            return InstantToken(name, faction)
        elif(token_type == TokenType.BOARD):
            return BoardToken(name, faction, data)
        raise ValueError(f"nie znaleziono żetonu o nazwie {name} z frakcji {faction}")