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
        return token.get_ability() == cls.ABILITY
        
    @staticmethod
    def can_execute(ctx : ActionContext, pos):
        return False

    @classmethod
    def can_use(cls, ctx : ActionContext, pos : Hex):
        # print(f"can use {}")
        return (
            cls.has_ability(ctx, pos)
            and cls.can_execute(ctx, pos)
        )
