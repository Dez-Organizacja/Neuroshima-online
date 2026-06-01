from main.engine.engine import GameEngine
from main.state.contex import ActionContext
from main.state.game_state import GameState
from main.rules.game import GameRules
from main.engine.resolver import Resolver
from main.workflows.data import WorkflowName, WorkflowConfig
from main.state.player_state import PlayerState

class Tests:
    def check_player(self, ctx : ActionContext, faction : str):
        player = ctx.state.players.get(faction, None)
        assert isinstance(player, PlayerState)
        assert not player.pile.empty
        if faction == ctx.faction:
            assert player.hand.size == 3
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
        assert ctx.workflow_instance.name == WorkflowName.TURN
        assert ctx.workflow_instance.current_step_index == 2
        assert isinstance(ctx.workflow_instance.config, WorkflowConfig)
        assert ctx.workflow_instance.config.faction in ["moloch", "borgo"]

        instance = ctx.state.workflow_stack[0]
        assert instance.name == WorkflowName.GAME
        assert sorted(instance.config.factions) == ["borgo", "moloch"]
        assert instance.current_step_index == 1
        self.check_player(ctx, "moloch")
        self.check_player(ctx, "borgo")