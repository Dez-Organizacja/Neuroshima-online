from ..builder import ScenarioBuilder
from ..registry import ScenarioRegistry
from ..data import Scenario
from main.input.data import BoardAction, HandAction, ActionType, RotationAction
from main.state.game_state import GameState
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName, WorkflowConfig
from ..delta_ops import *

@ScenarioRegistry.register("place_action")
def place_action_scenario() -> Scenario:
    factions = ["moloch", "borgo"]
    return (
        ScenarioBuilder(factions)
        .given(
            stack_add_game_wf(factions),
            stack_add_turn_wf(faction="moloch"),
            faction_delta("moloch"),
            hand_add(faction="moloch", card="klaun"),
            hand_add(faction="moloch", card="sieciarz"),
        )

        .when(HandAction(slot=0))
        .then(
            wf_data_delta(slot=0, type=ActionType.HAND),
            stack_index_change(index=4),
            stack_add(name=WorkflowName.HAND, index=1),
            stack_add(name=WorkflowName.PLACE, index=0),
        )

        .when(BoardAction(pos=(2, 4)))
        .then(
            tile_place(pos=(2, 4), name="klaun", faction="moloch"),
            stack_index_change(index=2),
            stack_add(name=WorkflowName.ROTATE, index=0),
            wf_data_delta(unit_pos=(2, 4), type=ActionType.BOARD),
            # hand_remove(faction="moloch", index=0),
            # wf_data_delta(slot=None, type=None),
            # stack_pop(), # pop place
            # stack_pop(), # pop hand
            # stack_index_change(index=2) # set turn wf index to waiting step
        )
        
        .when(RotationAction(rotation=1))
        .then(
            # tile_delta()
        )
    ).build()
