from main.engine.engine import GameEngine
from main.state.contex import ActionContext
from main.state.game_state import GameState
from main.rules.game import GameRules
from main.engine.resolver import Resolver
from main.workflows.data import WorkflowName, WorkflowConfig
from main.state.player_state import PlayerState
from main.input.data import BoardAction, Button, ButtonAction, HandAction, RotationAction

class Tests:
    def place_current_headquarter(
            self,
            engine : GameEngine,
            ctx : ActionContext,
            pos : tuple[int, int]
        ):
        faction = ctx.faction
        assert ctx.workflow_instance.name == WorkflowName.HEADQUARTER_TURN
        assert ctx.player.hand.tokens == ["sztab"]

        engine.execute_action(ctx, HandAction(slot=0))
        assert ctx.workflow_instance.name == WorkflowName.PLACE

        engine.execute_action(ctx, BoardAction(pos=pos))
        assert ctx.board.get_hq_pos(faction) == pos

        engine.execute_action(ctx, RotationAction(rotation=1))
        # assert ctx.workflow_instance.name == WorkflowName.HEADQUARTER_TURN
        return faction

    def check_player(self, ctx : ActionContext, faction : str):
        player = ctx.state.players.get(faction, None)
        assert isinstance(player, PlayerState)
        assert not player.pile.empty
        if faction == ctx.faction:
            assert player.hand.tokens == ["sztab"]
            assert "sztab" not in player.pile.tokens
        else:
            assert player.hand.size == 0

    def test_start_game(self):
        ctx = ActionContext(
            state=GameState(factions=["moloch", "borgo"]),
            rules=GameRules()
        )
        engine = GameEngine(Resolver())
        engine.start_game(ctx)

        assert len(ctx.state.workflow_stack) == 2
        assert ctx.workflow_instance.name == WorkflowName.HEADQUARTER_TURN
        assert ctx.workflow_instance.current_step_index == 2
        assert isinstance(ctx.workflow_instance.config, WorkflowConfig)
        assert ctx.workflow_instance.config.faction in ["moloch", "borgo"]

        instance = ctx.state.workflow_stack[0]
        assert instance.name == WorkflowName.GAME
        assert sorted(instance.config.factions) == ["borgo", "moloch"]
        assert instance.current_step_index == 1
        self.check_player(ctx, "moloch")
        self.check_player(ctx, "borgo")

    def test_hand_limits_in_first_turns(self):
        ctx = ActionContext(
            state=GameState(factions=["moloch", "borgo"]),
            rules=GameRules()
        )
        engine = GameEngine(Resolver())
        engine.start_game(ctx)

        first_hq_faction = self.place_current_headquarter(
            engine,
            ctx,
            ctx.board.ALL_HEXES[0],
        )
        second_hq_faction = self.place_current_headquarter(
            engine,
            ctx,
            ctx.board.ALL_HEXES[1],
        )

        assert {first_hq_faction, second_hq_faction} == {"moloch", "borgo"}
        assert ctx.workflow_instance.name == WorkflowName.TURN

        first_turn_faction = ctx.faction
        assert ctx.player.hand.size == 1

        engine.execute_action(ctx, ButtonAction(name = Button.END_TURN))
        second_turn_faction = ctx.faction
        assert second_turn_faction != first_turn_faction
        assert ctx.workflow_instance.name == WorkflowName.TURN
        assert ctx.player.hand.size == 2

        engine.execute_action(ctx, ButtonAction(name = Button.END_TURN))
        assert ctx.faction == first_turn_faction
        assert ctx.workflow_instance.name == WorkflowName.TURN
        assert ctx.player.hand.size == 3
