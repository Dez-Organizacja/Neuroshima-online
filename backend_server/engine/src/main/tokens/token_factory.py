from main.tokens.board_token import BoardToken
from main.tokens.base import Token
from main.tokens.data import TokenType
import main.frakcje.wszystkie_frakcje as allfractions
from main.tokens.registry import TokenConfigRegistry
from main.tokens.config import TokenConfigId

class TokenFactory():
    @staticmethod
    def create(name, faction):
        # print(f"create token request of name {name} and faction {faction}")
        config = TokenConfigRegistry.get(faction, name)
        config_id = TokenConfigId(name, faction)

        if(config.type == TokenType.INSTANT):
            return Token(config_id=config_id)
        elif(config.type == TokenType.BOARD):
            return BoardToken(config_id=config_id)
        raise ValueError(f"nie znaleziono żetonu o nazwie {name} z frakcji {faction}")