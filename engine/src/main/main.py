from main.state.game_state import GameState
from main.state.contex import ActionContext
from main.input.input_handler import InputHandler
from main.rules.validator import FormatValidator

from main.engine.engine import GameEngine
from main.engine.resolver import Resolver
from main.rules.game import GameRules

from main.systems.passive_systems import PassiveSystems
from main.view.builder import GameViewBuilder

from main.utils.variable import *

class Game:
    USER_ACTION_KEY = "user_action"
    TYPE_KEY = "message_type"
    def __init__(self, data : dict):
        self.state = GameState.from_dict(data)
        self.ctx = ActionContext(state=self.state, rules=GameRules())
        self.build_game_engine()

    def build_game_engine(self):
        self.engine = GameEngine(
            resolver                = Resolver(),
            passive_system          = PassiveSystems(),
        )
        self.input_handler = InputHandler(
            validator=FormatValidator(),
            engine=self.engine
        )
        self.game_view_builder = GameViewBuilder()

    def handle_action(self, data : dict):
        self.input_handler.handle_action(self.ctx, data)

    def build_user_view(self):
        return self.game_view_builder.build(self.ctx)

    def export(self):
        return{
            **self.state.to_dict(),
        }