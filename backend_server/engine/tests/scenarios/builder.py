from tests.workflows.scenarios import target

from .data import StepCase, Scenario, TileDelta, StackChange, Delta
from typing import Callable
from main.state.game_state import GameState
from main.input.data import UserAction
from main.workflows.data import WorkflowName, WorkflowInstance, WorkflowConfig

class ScenarioBuilder:
    def __init__(self, factions : list[str]):
        self.steps : list[StepCase] = []
        self.setup : Delta = Delta()
        self._current_step : StepCase | None = None
        self._factions : list[str] = factions

    def _requires_step(self):
        if(self._current_step is None):
            raise RuntimeError("Call when() first")

    
    @staticmethod
    def tile_delta(pos : tuple[int, int], **data):
        def apply(delta : Delta):
            delta.board_delta.append(TileDelta(pos=pos, unit=data))
        return apply
        
    @staticmethod
    def tile_remove(pos: tuple[int, int]):
        def apply(delta: Delta):
            delta.board_remove.append(pos)
        return apply

    @staticmethod
    def hand_add(card: str):
        def apply(delta: Delta):
            delta.hand_add.append(card)
        return apply
    
    @staticmethod
    def hand_remove(index: int):
        def apply(delta: Delta):
            delta.hand_remove.append(index)
        return apply
    
    @staticmethod
    def wf_data_delta(**data):
        def apply(delta: Delta):
            delta.wf_data_delta = data
        return apply
    
    @staticmethod
    def stack_add(
        name: WorkflowName,
        index: int | None = None,
        config: WorkflowConfig | None = None,
    ):
        def apply(delta: Delta):
            workflow_config = config or WorkflowConfig()

            delta.stack_delta.append(
                StackChange(
                    add=WorkflowInstance(
                        name=name,
                        index=index,
                        config=workflow_config,
                    )
                )
            )

        return apply
    
    @staticmethod
    def stack_pop():
        def apply(delta: Delta):
            delta.stack_delta.append(StackChange(pop=True))

        return apply

    @staticmethod
    def faction_delta(faction: str):
        def apply(delta: Delta):
            delta.faction_delta = faction

        return apply

    @staticmethod
    def expected_step_index(index: int):
        def apply(delta: Delta):
            delta.expected_step_index = index

        return apply
    
    def when(self, action : UserAction):
        step = StepCase(action=action)
        self._current_step = step
        self.steps.append(step)
        return self
    
    def then(self, *funcs : list[Callable[[Delta], None]]):
        self._requires_step()
        for func in funcs:
            func(self._current_step.delta)
        return self

    def given(self, *funcs : list[Callable[[GameState], None]]):
        self._requires_step()
        for func in funcs:
            func(self._current_step.setup)
        return self

    def build(self) -> Scenario:
        return Scenario(factions=self._factions, steps=self.steps)