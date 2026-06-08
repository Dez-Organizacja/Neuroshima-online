from main.state.contex import ActionContext
from main.tokens.base import Token

class PlacementRules:
    def can_discard(token : Token) -> bool:
        return not token.is_HQ