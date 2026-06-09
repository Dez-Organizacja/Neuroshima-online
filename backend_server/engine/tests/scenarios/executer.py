from .data import Scenario, StepCase
from main.main import Game
from main.state.game_state import GameState
from main.state.serialization import Serializator
from main.utils.diff import Diff

class ScenarioExecuter:
    def __init__(self):
        pass

    def get_expected_state(self, state : GameState, step: StepCase) -> dict:
        step.delta.apply(state)
        return Serializator.to_dict_dataclass(state)

    def run(self, scenario: Scenario):
        before_state = GameState(factions=scenario.factions)
        # print("SETUP")
        # print(scenario.setup)
        scenario.setup.apply(before_state)
        # print("before game state")
        # before_state.print_game_state()
        # print("----------------")
        
        for step in scenario.steps:

            # print("----------------------------------")
            # print("EXECUTER: executing step")
            # print(step)
            # print("----------------------------------")
            game = Game(Serializator.to_dict_dataclass(before_state))
            game.handle_action(Serializator.to_dict_dataclass(step.action))

            result_state = game.export()
            
            expected_state = self.get_expected_state(before_state, step)
            assert result_state == expected_state, Diff.compare(result_state, expected_state)

            before_state = Serializator.from_dict_dataclass(GameState, expected_state)

        # print("result state board")
        # print(result_state["board"])
        # assert False