import pytest
import main.events.effects as Ef
import main.events.flow as F
import main.events.workflow as WF
from main.state.contex import ActionContext
from main.state.game_state import GameState
from main.state.player_state import PlayerState
from main.rules.game import GameRules
from main.engine.resolver import Resolver
from main.events.data import ExecutionResult
from main.workflows.data import WorkflowInstance, WorkflowName, TurnConfig, WorkflowData

class Tests:
    @staticmethod
    def contex_maker() -> ActionContext:
        state = GameState(
            fractions=["moloch", "borgo"],
            current_fraction="moloch",
        )
        return ActionContext(state=state, rules=GameRules())

    def test1(self):
        ctx = self.contex_maker()
        ctx.state.players["moloch"] = PlayerState("moloch")
        ctx.player.hand.load_list(["klaun", "sieciarz"])
        ctx.player.pile.from_list(["lowca"])
        ctx.board.put_token((1, 3), "lowca", "moloch")
        ctx.board.put_token((1, 5), "lowca", "moloch")
        ctx.workflow_data = WorkflowData(slot=0, unit_pos=(1, 5))
        ctx.state.workflow_stack.extend([
            WorkflowInstance(name=WorkflowName.PLACE, current_step_index=0),
            WorkflowInstance(name=WorkflowName.TURN, config=TurnConfig("moloch"))
        ])

        effects = [
            Ef.DrawTokensEffect(hand_limit=3),
            Ef.DiscardTokenEffect(slot=0),
            Ef.PlaceEffect((2, 6), unit="klaun"),
            Ef.MoveEffect(from_pos=(1, 3), to_pos=(2, 2)),
            Ef.MarkAbilityUsedEffect((2, 6)),
            Ef.DamageEffect((1, 5), profile=Ef.DamageProfile()),
            Ef.RotateEffect(pos=(2, 2), rotation=1),
            Ef.ClearWorkflowDataEffect(),
            Ef.RemoveDeadUnitsEffect(positions=[(1, 5)])
        ]

        flows = [F.StartBattleEvent()]
        result = ExecutionResult(
            effects=effects,
            flow_events=flows
        )
        resolver = Resolver()
        resolver.resolve(result)

        assert(ctx.player.hand.to_list() == ["sieciarz", "lowca"])
        assert(ctx.player.pile.to_list() == [])
        
        assert(len(ctx.state.workflow_stack) == 1)
        assert(ctx.workflow_instance.name == WorkflowName.BATTLE)
        assert(ctx.workflow_instance.current_step_index == None)

        assert(ctx.board.get_token_position("klaun", "moloch") == (2, 6))
        assert(ctx.board.get_token((2, 6)).ability_used == True)

        assert(ctx.board.get_token_position("lowca", "moloch") == (2, 2))
        assert(ctx.board.get_token((2, 2)).ROTATION == 1)
        assert(ctx.board.get_token((1, 5)) is None)
        assert(ctx.board.get_token((1, 3)) is None)

        assert(ctx.workflow_data.slot is None)
        assert(ctx.workflow_data.unit_pos is None)

