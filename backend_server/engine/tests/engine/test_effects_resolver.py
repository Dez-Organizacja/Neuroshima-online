import main.events.effects as Ef
import main.events.flow as F
import main.events.workflow as Wf
from main.state.context import ActionContext
from main.state.game_state import GameState
from main.rules.game import GameRules
from main.engine.resolver import Resolver
from main.workflows.data import (
    WorkflowInstance, 
    WorkflowName, 
    WorkflowData, 
    WorkflowConfig
)
from main.rules.faction_manager import FactionManager

class Tests:
    @staticmethod
    def contex_maker() -> ActionContext:
        state = GameState(
            factions=["moloch", "borgo"],
            turn_faction="moloch",
            active_faction="moloch",
        )
        return ActionContext(
            state=state, 
            faction_manager=FactionManager(state.factions)
        )

    def test1(self):
        ctx = self.contex_maker()
        ctx.state.add_player("moloch")
        ctx.player.hand.tokens = ["klaun", "sieciarz"]
        ctx.player.pile.tokens = ["lowca"]
        ctx.board.put_token((1, 3), "lowca", "moloch")
        ctx.board.put_token((1, 5), "lowca", "moloch")
        ctx.state.workflow_data = WorkflowData(slot=0, unit_pos=(1, 5))
        ctx.state.workflow_stack.extend([
            WorkflowInstance(
                name=WorkflowName.TURN, 
                config=WorkflowConfig(faction="moloch")
            ),
            WorkflowInstance(name=WorkflowName.PLACE, current_step_index=0),
        ])

        effects = [
            Ef.DrawTokensEffect(hand_limit=3),
            Ef.DiscardTokenEffect(slot=0),
            Ef.PlaceEffect((2, 6), ctx.player.hand.get(0), "moloch"),
            Ef.MoveEffect(from_pos=(1, 3), to_pos=(2, 2)),
            Ef.DamageEffect(pos=(1, 5)),
            Ef.RotateEffect(pos=(2, 2), rotation=1),
            Ef.ClearWorkflowDataEffect(),
            Ef.ResolveUnitsDamageEffect(positions=[(1, 5)])
        ]

        flows = [F.EndTurnEvent()]
        result = effects + flows
        # print(result)
        resolver = Resolver()
        resolver.execute(ctx=ctx, result=result)
        resolver.execute(ctx=ctx, result=[Wf.PushWorkflow(name=WorkflowName.BATTLE)])

        assert(ctx.faction == "")
        ctx.faction = "moloch"
        assert(ctx.player.hand.tokens == ["sieciarz", "lowca"])
        assert(ctx.player.pile.tokens == [])
        
        assert(len(ctx.state.workflow_stack) == 1)
        assert(ctx.workflow_instance.name == WorkflowName.BATTLE)
        assert(ctx.workflow_instance.current_step_index == None)

        assert(ctx.board.get_token_position("lowca", "moloch") == (2, 2))
        assert(ctx.board.get_token((2, 2)).state.rotation == 1)
        assert(ctx.board.get_token((1, 5)) is None)
        assert(ctx.board.get_token((1, 3)) is None)

        assert(ctx.workflow_data.slot is None)
        assert(ctx.workflow_data.unit_pos is None)

        # assert False
        # assert(len(ctx.state.workflow_stack) == 1)