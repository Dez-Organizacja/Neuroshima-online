from main.state.game_state import GameState
from main.state.context import ActionContext
from main.input.input_handler import InputHandler
from main.rules.validator import FormatValidator

from main.engine.engine import GameEngine
from main.engine.resolver import Resolver
from main.rules.faction_manager import FactionManager
from main.systems.undo import UndoSystem

from main.view.builder import GameViewBuilder
from main.state.game_dump import GameDump

from main.utils.variable import *
from main.bootstrap import bootstrap


class Game:
    def __init__(self):
        bootstrap()
        self.undo_system = UndoSystem()
        self.build_game_engine()

    def load(self, data : dict):
        dump = GameDump.from_dict(data)
        self.state : GameState = GameState.from_dict(dump.state)
        self.undo_system = UndoSystem(dump.undo)


    def build_game_engine(self):
        self.engine = GameEngine(resolver = Resolver())
        self.input_handler = InputHandler(
            validator=FormatValidator(),
            engine=self.engine
        )
        self.game_view_builder = GameViewBuilder()

    def build_context(self) -> ActionContext:
        return ActionContext(
            state=self.state,
            faction_manager=FactionManager(self.state.factions),
            undo_system=self.undo_system,
        )

    def handle_action(self, data : dict):
        ctx = self.build_context()
        self.input_handler.handle_action(ctx, data)
        self.state = ctx.state

    def build_user_view(self):
        return self.game_view_builder.build(self.build_context())

    def start_game(self, data : dict):
        self.state = GameState.from_dict(data)
        return self.engine.start_game(self.build_context())

    def export(self) -> dict:
        dump = GameDump(
            state=self.state.to_dict(),
            undo=self.undo_system.to_list()
        )
        # print("exporting")
        # print(f"undo: {dump.undo}")
        # print(f"state: {dump.state}")
        # print(f"dicted: {dump.to_dict()}")
        return dump.to_dict()