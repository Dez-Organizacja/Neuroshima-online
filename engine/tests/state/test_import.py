import json
from collections import deque

from main.state.game_state import GameState
from main.workflows.data import WorkflowInstance, TurnConfig, WorkflowName
from main.events.data import FlowEvent

def test_game_state_serialization_roundtrip():

    # GIVEN
    state = GameState(
        fractions=["moloch", "borgo"],
        current_fraction="moloch"
    )

    state.add_player("moloch")
    state.add_player("morgo")
    state.board.put_token((1, 1), "klaun", "moloch")
    
    state.workflow_stack.append(
        WorkflowInstance(
            name=WorkflowName.TURN,
            config=TurnConfig("borgo"),
            current_step_index=2
        )
    )

    # WHEN
    data = state.to_dict()
    json_string = json.dumps(data)

    # # THEN
    loaded_data = json.loads(json_string)

    restored_state : GameState = GameState.from_dict(loaded_data)
    restored_data = restored_state.to_dict()

    assert restored_data == data