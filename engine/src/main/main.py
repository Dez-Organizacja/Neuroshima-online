from main.state.game_state import GameState
from main.state.contex import ActionContext
from main.input.input_handler import InputHandler
from main.rules.validator import FormatValidator

from main.engine.engine import GameEngine
from main.engine.resolver import Resolver
from main.rules.game import GameRules

from main.view.builder import GameViewBuilder

from main.utils.variable import *

class Game:
    def __init__(self, data : dict):
        self.state = GameState.from_dict(data)
        self.rules = GameRules()
        self.build_game_engine()

    def build_game_engine(self):
        self.engine = GameEngine(resolver = Resolver())
        self.input_handler = InputHandler(
            validator=FormatValidator(),
            engine=self.engine
        )
        self.game_view_builder = GameViewBuilder()

    def build_contex(self) -> ActionContext:
        return ActionContext(state=self.state, rules=self.rules)

    def handle_action(self, data : dict):
        self.input_handler.handle_action(self.build_contex(), data)

    def build_user_view(self):
        return self.game_view_builder.build(self.build_contex())

    def start_game(self):
        return self.engine.start_game(self.build_contex())

    def export(self):
        return{
            **self.state.to_dict(),
        }