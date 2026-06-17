from main.engine.engine import GameEngine
from main.engine.resolver import Resolver
from main.input.data import BoardAction, RotationAction
from main.rules.game import GameRules
from main.state.context import ActionContext
from main.state.game_state import GameState
from main.view.builder import GameViewBuilder
from main.workflows.data import WorkflowConfig, WorkflowInstance, WorkflowName
# from main.workflows.providers.turn import TurnProvider
from main.workflows.providers.action import ActionProvider
from main.rules.faction_manager import FactionManager

def make_ctx() -> ActionContext:
    state = GameState(
        factions=["posterunek", "moloch"],
        turn_faction="posterunek",
        active_faction="posterunek"
    )
    return ActionContext(
        state=state, 
        faction_manager=FactionManager(state.factions)
    )


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
    engine.run_until_input_required(ctx)
    engine.execute_action(ctx, BoardAction(pos=(1, 1)))

    assert ctx.workflow_instance.name == WorkflowName.MOVE
    assert ctx.workflow_instance.current_step_index == 1

    engine.execute_action(ctx, BoardAction(pos=(1, 3)))
    engine.execute_action(ctx, RotationAction(rotation=1))
    moved = ctx.board.get_token((1, 3))
    assert ctx.board.get_token((1, 1)) is None
    assert moved.name == "biegacz"
    assert moved.ability_used is True
    assert moved.rotation == 1
    assert ctx.workflow_instance.name == WorkflowName.ACTION


def test_turn_provider_hides_wired_ability_units():
    ctx = make_ctx()
    ctx.board.put_token((1, 1), "biegacz", "posterunek")
    ctx.board.get_token((1, 1)).set_wire()

    assert (1, 1) not in ActionProvider().get_available_positions(ctx)


def test_borgo_move_ability_is_visible_in_available_actions_board():
    state = GameState(
        factions=["borgo", "moloch"],
        turn_faction="borgo",
        active_faction="borgo",
    )
    ctx = ActionContext(
        state=state, 
        faction_manager=FactionManager(state.factions)
    )
    ctx.state.add_player("borgo")

    ctx.board.put_token((1, 5), "zabojca", "borgo")
    ctx.state.workflow_stack.append(
        WorkflowInstance(
            name=WorkflowName.TURN,
            current_step_index=2,
            config=WorkflowConfig(faction="borgo"),
        )
    )
    engine = GameEngine(resolver=Resolver())
    engine.run_until_input_required(ctx)

    view = GameViewBuilder().build(ctx)

    assert view["availableActions"]["board"] == [[1, 5]]

# def test_centrum_rozpoznania_gives_moves_of_range_two():
