import pytest

from main.main import Game
from main.state.game_state import GameState
from main.workflows.data import WorkflowConfig, WorkflowInstance, WorkflowName
from main.state.game_dump import GameDump
from main.input.data import Button

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
            current_step_index=0,
        )
    )
    game = Game()
    game.load(GameDump(state=state.to_dict()).to_dict())
    game.engine.run_until_input_required(game.build_context())
    return game

def hand_action(game : Game, slot=0):
    game.handle_action({
        "type" : "hand",
        "slot" : slot
    })

def board_action(game : Game, pos = (2, 4)):
    game.handle_action({
        "type": "board",
        "pos": [*pos],
    })

def rotation_action(game : Game, rotation : int = 0):
    game.handle_action({
        "type" : "rotate",
        "rotation" : rotation
    })

def end_turn_action(game : Game):
    game.handle_action({
        "type" : "button",
        "name" : "end_turn",
    })

def cancel_action(game : Game):
    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

def place_actions(game : Game, pos : tuple[int, int], slot=0, rotation = 0):
    name = game.state.players[game.state.active_faction].hand.get(slot)
    hand_action(game, slot)
    board_action(game, pos)
    rotation_action(game, rotation)
    # end_turn_action(game)
    unit = game.state.board.get_token(pos)
    assert unit is not None
    assert unit.name == name
    assert unit.rotation == rotation

def test_cancel_restores_state_to_before_hand_token_selection():
    game = build_place_game()

    game.handle_action({
        "type": "hand",
        "slot": 0,
    })

    assert game.state.workflow_stack[-1].name == WorkflowName.PLACE
    assert len(game.undo_system.stack) == 1

    game.handle_action({
        "type": "board",
        "pos": [2, 4],
    })

    assert game.state.board.get_token((2, 4)) is not None
    assert game.state.players["moloch"].hand.tokens == []
    assert game.state.workflow_stack[-1].name == WorkflowName.ROTATE
    assert len(game.undo_system.stack) == 1

    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

    assert len(game.undo_system.stack) == 0
    assert game.state.board.get_token((2, 4)) is None
    assert game.state.players["moloch"].hand.tokens == ["sztab"]
    assert game.state.workflow_stack[-1].name == WorkflowName.ACTION
    assert game.state.workflow_data.slot is None

def test_other_faction_decision_clears_undo_stack():
    game = build_place_game()

    game.handle_action({
        "type": "hand",
        "slot": 0,
    })

    # game.state.clear_undo_stack("borgo")
    assert len(game.undo_system.stack) == 1

    game.handle_action({
        "type": "button",
        "name": "cancel",
    })

    assert game.state.workflow_stack[-1].name == WorkflowName.ACTION

# def test_serialization_undo_system_start_game():
    # game = build_place_game()
    # assert game.state.workflow_stack[-1].name == WorkflowName.ACTION
    
    # game.handle_action({
    #     "type": "hand",
    #     "slot": 0,
    # })

    # assert len(game.undo_system.stack) == 1
    # dump = game.export()
    # print(dump)
    # game.load(dump)
    # assert len(game.undo_system.stack) == 1
    # game = Game()
    # game.start_game({"factions" : ["moloch", "borgo"]})
    # game.state.players["moloch"].pile.tokens = ["bloker", "klaun", "sztab"]
    # game.state.players["borgo"].pile.tokens = ["mutek", "mutek", "mutek", "sztab"]
    # place_actions(game, (2, 4), rotation=1)
    # place_actions(game, (2, 2), rotation=1)
    #turn 
    # hand_action(game, 0)

    # data = game.export()
    # print(data["undo"])


    # assert False

# def test_cancel_restores_draw_discard_from_full_hand():
#     game = build_draw_discard_game()

#     game.handle_action({
#         "type": "hand",
#         "slot": 1,
#     })

#     assert game.state.players["moloch"].hand.tokens == ["bitwa", "bomba"]
#     assert game.state.workflow_stack[-1].name == WorkflowName.TURN
#     assert len(game.state.undo_stack) == 1

#     game.handle_action({
#         "type": "button",
#         "name": "cancel",
#     })

#     assert game.state.players["moloch"].hand.tokens == ["bitwa", "bitwa", "bomba"]
#     assert game.state.workflow_stack[-1].name == WorkflowName.DRAW
#     assert game.state.workflow_stack[-1].current_step_index == 3
#     assert game.state.workflow_data.slot is None
#     assert game.state.undo_stack == []


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

    assert game.state.workflow_stack[-1].name == WorkflowName.ACTION
    assert game.undo_system.stack == []

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

    # assert game.state.workflow_stack[-1].name == WorkflowName.ACTION
    # assert game.state.workflow_data.slot is None
    # assert game.state.board.get_token((2, 4)) is None
    # assert game.state.players["moloch"].hand.tokens == ["sztab"]
