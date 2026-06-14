from .data import StepCase, Scenario, Delta
from typing import Callable
from main.state.game_state import GameState
from main.input.data import UserAction, Button
from main.actions.available.data import AvailableStructure

class ScenarioBuilder:
    def __init__(self, factions : list[str]):
        self.factions = factions
        self.steps : list[StepCase] = []
        self.setup : Delta = Delta()
        self._current_step : StepCase | None = None

    def _requires_step(self):
        if(self._current_step is None):
            raise RuntimeError("Call when() first")
    
    def when(self, action : UserAction):
        step = StepCase(action=action)
        self._current_step = step
        self.steps.append(step)
        return self
    
    def then(self, *funcs : list[Callable[[Delta], None]]):
        self._requires_step()
        self._current_step.delta.add(*funcs)
        return self

    def available_actions(
            self,
            *funcs : list[Callable[[AvailableStructure], None]]
    ):
        self._requires_step()
        self._current_step.available_actions = AvailableStructure()

        for func in funcs:
            func(self._current_step.available_actions)
        return self
        

    def given(self, *funcs : list[Callable[[GameState], None]]):
        self.setup.add(*funcs)
        return self

    def build(self) -> Scenario:
        return Scenario(
            factions=self.factions,
            steps=self.steps, 
            setup=self.setup
        )