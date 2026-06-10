from .data import Scenario, StepCase
from main.main import Game
from main.state.game_state import GameState
from main.state.serialization import Serializator
from main.utils.diff import Diff
from main.view.state import StateViewBuilder
from main.view.step import StepViewBuilder
from main.actions.available.data import AvailableStructure
from main.systems.passive_systems import PassiveSystems

class ScenarioExecuter:
    def __init__(self):
        pass

    @staticmethod
    def get_state_data(state : GameState) -> dict:
        state_data = Serializator.to_dict_dataclass(state)
        state_data["board"] = StateViewBuilder.build_board_view(state)
        return state_data

    @staticmethod
    def execute(before_state : GameState, step : StepCase) -> Game:
        print("----------------------------------")
        print("EXECUTER: executing step")
        print(step)
        print("----------------------------------")
        game = Game(Serializator.to_dict_dataclass(before_state))
        game.handle_action(Serializator.to_dict_dataclass(step.action))
        return game

    def validate_state(self, result_state : GameState, expected_state : GameState):
        result_data = self.get_state_data(result_state)
        # print("result board")
        # result_state.board.print_board()

        expected_data = self.get_state_data(expected_state)
        assert result_data == expected_data, Diff.compare(result_data, expected_data)

    @staticmethod
    def compare_av_actions(game : Game, expected_actions : AvailableStructure):
        
        step_view = StepViewBuilder().build_step(game.build_contex())
        result_actions = step_view.available_actions
        assert result_actions == expected_actions, Diff.compare(result_actions, expected_actions)

    def run(self, scenario: Scenario):
        before_state = GameState(factions=scenario.factions)
        # print("SETUP")
        # print(scenario.setup)
        scenario.setup.apply(before_state)
        PassiveSystems.compute(before_state.board)

        print("AT (1, 3)", before_state.board.get_token((1, 3)))
        print("is wired:", before_state.board.get_token((1, 3)).wired)

        # print("before game state")
        # before_state.print_game_state()
        # print("----------------")
        
        for step in scenario.steps:
            game = self.execute(before_state, step)
            step.delta.apply(before_state)

            self.validate_state(game.state, before_state)
            if step.available_actions is not None:
                self.compare_av_actions(game, step.available_actions)
            
            before_state = game.state

        # print("result state board")
        # print(result_state["board"])
        # assert False