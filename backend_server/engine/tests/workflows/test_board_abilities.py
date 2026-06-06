from main.engine.engine import GameEngine
from main.engine.resolver import Resolver
from main.input.data import BoardAction
from main.rules.game import GameRules
from main.state.contex import ActionContext
from main.state.game_state import GameState
from main.view.builder import GameViewBuilder
from main.workflows.data import WorkflowConfig, WorkflowInstance, WorkflowName
from main.workflows.providers.turn import TurnProvider


def make_ctx() -> ActionContext:
    state = GameState(
        factions=["posterunek", "moloch"],
        current_faction="posterunek",
    )
    return ActionContext(state=state, rules=GameRules())


def test_board_move_ability_moves_selected_unit_and_marks_it_used():
    ctx = make_ctx()
    ctx.board.put_token((1, 1), "biegacz", "posterunek")
    ctx.state.workflow_stack.append(
        WorkflowInstance(
            name=WorkflowName.TURN,
            current_step_index=2,
            config=WorkflowConfig(faction="posterunek"),
        )
    )

    engine = GameEngine(Resolver())
    engine.execute_action(ctx, BoardAction(pos=(1, 1)))

    assert ctx.workflow_instance.name == WorkflowName.MOVE
    assert ctx.workflow_instance.current_step_index == 1

    engine.execute_action(ctx, BoardAction(pos=(1, 3)))

    moved = ctx.board.get_token((1, 3))
    assert ctx.board.get_token((1, 1)) is None
    assert moved.name == "biegacz"
    assert moved.ability_used is True
    assert ctx.workflow_instance.name == WorkflowName.TURN


def test_turn_provider_hides_wired_ability_units():
    ctx = make_ctx()
    ctx.board.put_token((1, 1), "biegacz", "posterunek")
    ctx.board.get_token((1, 1)).set_wire()

    assert (1, 1) not in TurnProvider().get_available_positions(ctx)


def test_borgo_move_ability_is_visible_in_available_actions_board():
    state = GameState(
        factions=["borgo", "moloch"],
        current_faction="borgo",
    )
    ctx = ActionContext(state=state, rules=GameRules())
    ctx.board.put_token((1, 5), "zabojca", "borgo")
    ctx.state.workflow_stack.append(
        WorkflowInstance(
            name=WorkflowName.TURN,
            current_step_index=2,
            config=WorkflowConfig(faction="borgo"),
        )
    )

    view = GameViewBuilder().build(ctx)

    assert view["availableActions"]["board"] == [[1, 5]]
