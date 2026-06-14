from .data import Scenario, StepCase
from main.main import Game
from main.state.game_state import GameState
from main.state.serialization import Serializator
from main.utils.diff import Diff
from main.view.step import StepViewBuilder
from main.actions.available.data import AvailableStructure
from main.systems.passive_systems import PassiveSystems
from main.input.data import Button
from main.utils.diff_state import DiffState

class ScenarioExecuter:
    def __init__(self):
        pass

    @staticmethod
    def init_game(state : GameState) -> Game:
        data = Serializator.to_dict_dataclass(state)
        # print(data)
        return Game(data)

    def execute(self, before_state : GameState, step : StepCase) -> Game:
        print("----------------------------------")
        print("EXECUTER: executing step")
        print(f"action {step.action}")
        print("----------------------------------")
        # print("BEFORE STATE")
        game = self.init_game(before_state)
        # print("INITIALIZED GAME")
        game.handle_action(Serializator.to_dict_dataclass(step.action))
        return game

    @staticmethod
    def compare_av_actions(game : Game, expected_actions : AvailableStructure):

        step_view = StepViewBuilder().build_step(game.build_contex())
        result_actions = step_view.available_actions
        if Button.CANCEL not in expected_actions.buttons:
            result_actions.buttons = [
                button for button in result_actions.buttons
                if button != Button.CANCEL
            ]
        assert result_actions == expected_actions, Diff.compare(result_actions, expected_actions)

    def setup(self, scenario : Scenario) -> GameState:
        before_state = GameState(factions=scenario.factions)
        scenario.setup.apply(before_state)
        PassiveSystems.compute(before_state.board)
        game = self.init_game(before_state)
        game.engine.run_until_input_required(game.build_contex())
        # print(game.state.workflow_stack[-1])
        return game.state

    def run(self, scenario: Scenario):
        # print("RUNNING SCENARIO")
        # print(scenario.setup)
        before_state = self.setup(scenario)
        # print
        # print("before game state")
        # before_state.print_game_state()
        # print("----------------")
        
        for step in scenario.steps:
            if(step.finish):
                break

            game = self.execute(before_state, step)
            step.delta.apply(before_state)


            print("result")
            # game.state.board.print_board()
            print(game.state.workflow_stack[-1])
            print(game.state.players["moloch"].hand)
            # print(f"active faction: {game.state.active_faction}")
            # print(f"turn faction: {game.state.turn_faction}")
            DiffState.compare(game.state, before_state)
            # print("COMPARED SUCCESUFULLY")

            if step.available_actions is not None:
                self.compare_av_actions(game, step.available_actions)
            
            before_state = game.state