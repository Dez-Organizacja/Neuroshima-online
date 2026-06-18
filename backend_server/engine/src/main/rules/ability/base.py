from abc import ABC, abstractmethod
from main.state.context import ActionContext
from main.board.data import Hex
from main.tokens.data import Ability

class AbilityRules(ABC):
    ABILITY : Ability | None = None

    @staticmethod
    def get_sources(ctx : ActionContext):
        return []
    
    @staticmethod
    def get_targets(ctx : ActionContext):
        return []

    @staticmethod
    def get_destinations(ctx : ActionContext):
        return []
    
    @classmethod
    def has_ability(cls, ctx : ActionContext, pos : Hex):
        token = ctx.board.get_token(pos)
        print(token.get_ability())
        return (
            token.get_ability() == cls.ABILITY
            and token.has_unused_ability()
        )
        
    @staticmethod
    def can_execute(ctx : ActionContext, pos):
        return False

    @classmethod
    def can_use(cls, ctx : ActionContext, pos : Hex):
        # print(f"check can use {cls.ABILITY} at {pos}")
        return (
            cls.has_ability(ctx, pos)
            and cls.can_execute(ctx, pos)
        )
