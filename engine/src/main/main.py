from main.state.game_state import GameState
from main.state.contex import ActionContext
from main.state.user_action import UserActionFactory

from main.rules.game import GameRules
from main.rules.validator import FormatValidator

from main.engine.engine import GameEngine
from main.engine.resolver import Resolver

from main.systems.passive_system import PassiveSystem

from main.actions.exeute_actions.execute_action import Actions
from main.actions.available_actions.available_actions import AvailableActions
from main.utils.variable import *

class Game:
    USER_ACTION_KEY = "user_action"
    AVAILABLE_ACTIONS_KEY = "available_actions"
    def __init__(self, data):
        fractions = data['fractions']
        if(isinstance(fractions, dict)):
            data['fractions'] = [fractions["player1"], fractions["player2"]]
        
        self.state = GameState.from_dict(data)
        self.build_game_engine()
        self.ctx = ActionContext(self.state, self.rules)

        if self.state.phase in (Phase.START_GAME, Phase.START_GAME.value):
            self.available_actions = self.engine.start_game(self.ctx)

        else:
            self.user_action = UserActionFactory.create(
                data.get(self.USER_ACTION_KEY, {})
            )
            self.available_actions = self.engine.handle_action(
                ctx = self.ctx, 
                action = self.user_action
            )

    def build_game_engine(self):
        self.rules = GameRules()
        
        self.engine = GameEngine(
            rules                   = self.rules,
            resolver                = Resolver(),
            passive_system          = PassiveSystem(),
            validator               = FormatValidator(),
            actions                 = Actions(),
            available_actions       = AvailableActions()
        )

    def export(self):
        return{
            **self.state.to_dict(),
            self.AVAILABLE_ACTIONS_KEY : self.available_actions
        }