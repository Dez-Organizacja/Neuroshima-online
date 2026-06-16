from main.tokens.base import Token

class PlacementRules:
    @staticmethod
    def can_discard(token : Token) -> bool:
        return not token.is_HQ