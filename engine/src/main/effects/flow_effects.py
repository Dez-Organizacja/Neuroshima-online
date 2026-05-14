from main.state.contex import ActionContext
from main.utils.variable import Turn, Phase
from main.actions.exeute_actions.action_result import ActionResult
from main.effects.ui_change_effects import ResetInteraction
from main.battle.battle import Battle
from main.workflows.data import WorkflowSource
from main.workflows.data import WorkflowName
from main.workflows.base import WorkflowFactory

class FlowEvent:
    pass

class EndTurnEvent(FlowEvent):
    def apply(self, ctx : ActionContext):
        next_turn = ctx.state.next_turns[0]
        fraction = next_turn[Turn.FRACTION]

        ctx.state.next_turns.pop(0)
        ctx.state.next_turns.append({
            Turn.FRACTION : fraction, 
            Turn.TYPE : Turn.Type.STANDARD
        })

        return ActionResult(interaction_state_changes=[ResetInteraction()])


class BeginTurnEvent(FlowEvent):
    def apply(self, ctx : ActionContext):
        fraction = ctx.state.next_turns[0][Turn.FRACTION]
        type = ctx.state.next_turns[0][Turn.TYPE]
        ctx.state.current_fraction = fraction
        
        if(type == Turn.Type.HQ_PLACEMENT):
            ctx.state.phase = Phase.HQ_PLACEMENT
        else:
            ctx.state.phase = Phase.GAME

        ctx.player.draw_tokens(type)

class StartBattleEvent(FlowEvent):
    def __init__(self, attacker, defender):
        super().__init__()
        self.attacker = attacker
        self.defender = defender
    
    def apply(self, ctx):
        ctx.flow_queue.append(EndTurnEvent())
        ctx.flow_queue.append(ResolveBattleEvent())

class ResolveBattleEvent(FlowEvent):
    def setup_battle(self, ctx):
        ctx.phase = Phase.BATTLE
        Battle(ctx)
        return ActionResult(flow_events=[BeginTurnEvent()])

class SwapPlayerEvent(FlowEvent):
    def apply(self, ctx : ActionContext):
        ctx.state.current_fraction = ctx.rules.get_enemy(ctx, ctx.fraction)

# class StartWorkflow(FlowEvent):
#     def __init__(self, 
#                  name   : WorkflowName,
#                  source : WorkflowSource | None = None
#         ):
#         super().__init__()
#         self.source = source
#         self.name = name
    
#     def apply(self, ctx : ActionContext):
#         ctx.workflow = WorkflowFactory.create(self.name)
#         ctx.workflow.start(ctx, self.source)