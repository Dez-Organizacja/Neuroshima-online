import pytest

from main.main import Game
from main.state.game_state import GameState
from main.workflows.data import WorkflowConfig, WorkflowInstance, WorkflowName


def build_place_game() -> Game:
    state = GameState(
        factions=["moloch", "borgo"],
        turn_faction="moloch",
        active_faction="moloch",
    )
    state.players["moloch"].hand.add("sztab")
    state.workflow_stack.append(
        WorkflowInstance(
            name=WorkflowName.TURN,
            config=WorkflowConfig(faction="moloch"),
            current_step_index=2,
        )
    )
    return Game(state.to_dict())


def test_cancel_restores_state_to_before_hand_token_selection():
    game = build_place_game()

    game.handle_action({
        "type": "hand",
        "slot": 0,
    })

    assert game.state.workflow_stack[-1].name == WorkflowName.PLACE
    assert len(game.state.undo_stack) == 1

    game.handle_action({
        "type": "board",
        "pos": [2, 4],
    })

    assert game.state.board.get_token((2, 4)) is not None
    assert game.state.players["moloch"].hand.tokens == []
    assert game.state.workflow_stack[-1].name == WorkflowName.ROTATE

    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

    assert game.state.board.get_token((2, 4)) is None
    assert game.state.players["moloch"].hand.tokens == ["sztab"]
    assert game.state.workflow_stack[-1].name == WorkflowName.TURN
    assert game.state.workflow_data.slot is None
    assert game.state.undo_stack == []


def test_other_faction_decision_clears_undo_stack():
    game = build_place_game()

    game.handle_action({
        "type": "hand",
        "slot": 0,
    })

    game.state.clear_undo_stack("borgo")
    assert game.state.undo_stack == []

    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

    assert game.state.workflow_stack[-1].name == WorkflowName.TURN


def test_cancel_can_restore_new_snapshot_after_previous_restore():
    game = build_place_game()

    game.handle_action({
        "type": "hand",
        "slot": 0,
    })
    game.handle_action({
        "type": "board",
        "pos": [2, 4],
    })
    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

    assert game.state.workflow_stack[-1].name == WorkflowName.TURN
    assert game.state.undo_stack == []

    game.handle_action({
        "type": "hand",
        "slot": 0,
    })
    game.handle_action({
        "type": "board",
        "pos": [2, 4],
    })
    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

    assert game.state.workflow_stack[-1].name == WorkflowName.TURN
    assert game.state.workflow_data.slot is None
    assert game.state.board.get_token((2, 4)) is None
    assert game.state.players["moloch"].hand.tokens == ["sztab"]
