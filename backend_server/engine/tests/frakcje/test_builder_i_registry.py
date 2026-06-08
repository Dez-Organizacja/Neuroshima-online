from main.tokens.registry import TokenConfigRegistry
from main.tokens.data import TokenType
from main.tokens.config import BoardTokenConfig

def test():
    config : BoardTokenConfig = TokenConfigRegistry.get("moloch", "bloker")
    assert config.hp == 3
    assert config.unit_count == 2
    assert config.type == TokenType.BOARD
    assert config.armor == [0]