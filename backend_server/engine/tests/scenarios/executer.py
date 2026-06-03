from .data import Scenario, StepCase
from main.main import Game
from main.state.game_state import GameState
from main.state.serialization import Serializator

class ScenarioExecuter:
    def __init__(self):
        pass

    def get_expected_state(self, state : GameState, step: StepCase) -> GameState:
        if step.expected_step_index is not None:
            state.step_index = step.expected_step_index
        
        if step.faction_delta is not None:
            state.current_faction = step.faction_delta

        for delta in step.board_delta:
            token = state.board.get_token(delta.pos)
            for key, value in delta.unit.items():
                setattr(token, key, value)
        
        for pos in step.board_remove:
            state.board.remove_token(pos)

        for token in step.hand_add:
            state.hand.add_token(token)
        
        for index in step.hand_remove:
            state.hand.remove_token(index)

        for key, value in step.wf_data_delta.items():
            setattr(state.workflow_data, key, value)
        
        for change in step.stack_delta:
            if change.pop:
                state.stack.pop()
            if change.add is not None:
                state.stack.append(change.add)

        return Serializator.to_dict_dataclass(state)


    def run(self, scenario: Scenario):
        before_state = GameState(factions=scenario.factions)
        if scenario.setup_function:
            scenario.setup_function(before_state)
        
        for step in scenario.steps:
            
            game = Game(Serializator.to_dict_dataclass(before_state))
            game.handle_action(Serializator.to_dict_dataclass(step.action))

            result_state = game.export()
            expected_state = self.get_expected_state(before_state, step)
            assert result_state == expected_state

            before_state = Serializator.from_dict_dataclass(GameState, expected_state)