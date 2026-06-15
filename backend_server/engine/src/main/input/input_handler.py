from main.input.data import UserActionFactory
from main.engine.engine import GameEngine
from main.rules.validator import FormatValidator
from main.state.context import ActionContext

class InputHandler:
    def __init__(self,
                 validator : FormatValidator,
                 engine : GameEngine,
        ):
        self.validator = validator
        self.engine = engine

    def handle_action(self, ctx : ActionContext, action : dict):
        if not self.validator.is_valid_action(action):
            raise ValueError("invalid action format")
        
        action_instance = UserActionFactory.create(action)
        self.engine.execute_action(ctx, action_instance)