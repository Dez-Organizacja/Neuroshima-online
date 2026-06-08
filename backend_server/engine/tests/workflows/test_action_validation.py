import pytest

from main.input.data import HandAction
from main.main import Game
from main.state.game_state import GameState
from main.workflows.data import WorkflowConfig, WorkflowInstance, WorkflowName
from main.workflows.factory import WorkflowFactory
from main.workflows.providers.movement import RotateProvider

from .fakes import FakeContext


def test_move_workflow_rejects_hand_action_when_board_position_is_expected():
    ctx = FakeContext(
        workflow_instance=WorkflowInstance(
            name=WorkflowName.MOVE,
            current_step_index=0,
        )
    )
    workflow = WorkflowFactory.create(ctx.workflow_instance)
    workflow.build_steps()

    with pytest.raises(ValueError, match="nie jest dozwolona"):
        workflow.get_current_step(ctx).execute(ctx, HandAction(slot=0))


def test_rotate_provider_does_not_emit_null_board_position():
    ctx = FakeContext(
        workflow_instance=WorkflowInstance(
            name=WorkflowName.ROTATE,
            current_step_index=0,
        )
    )

    assert RotateProvider().get_available_positions(ctx) == []


def test_move_view_can_be_built_after_selecting_move_instant():
    state = GameState(
        factions=["moloch", "hegemonia"],
        current_faction="hegemonia",
    )
    state.board.put_token((2, 4), "sztab", "moloch")
    state.board.put_token((1, 1), "sztab", "hegemonia")
    state.board.put_token((1, 3), "biegacz", "hegemonia")
    state.players["hegemonia"].hand.add("ruch")
    state.workflow_data.slot = 0
    state.workflow_data.type = "hand"
    state.workflow_stack = [
        WorkflowInstance(
            name=WorkflowName.GAME,
            current_step_index=4,
            config=WorkflowConfig(factions=["moloch", "hegemonia"]),
        ),
        WorkflowInstance(
            name=WorkflowName.TURN,
            current_step_index=4,
            config=WorkflowConfig(faction="hegemonia", hand_limit=2),
        ),
        WorkflowInstance(
            name=WorkflowName.HAND,
            current_step_index=1,
        ),
        WorkflowInstance(
            name=WorkflowName.MOVE,
            current_step_index=0,
        ),
    ]

    view = Game(state.to_dict()).build_user_view()

    assert [1, 1] in view["availableActions"]["board"]
    assert [1, 3] in view["availableActions"]["board"]
