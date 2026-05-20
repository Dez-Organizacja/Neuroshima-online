from main.events.base import Event
from abc import ABC
from main.state.contex import ActionContext
from main.utils.variable import Turn, Phase
class FlowEvent(ABC, Event):
    pass

class StartTurnEvent(FlowEvent):
    def apply(self, ctx : ActionContext):
        fraction = ctx.state.next_turns[0][Turn.FRACTION]
        type = ctx.state.next_turns[0][Turn.TYPE]
        ctx.state.current_fraction = fraction
        
        if(type == Turn.Type.HQ_PLACEMENT):
            ctx.state.phase = Phase.HQ_PLACEMENT
        else:
            ctx.state.phase = Phase.GAME

        ctx.player.draw_tokens(type)

class EndTurnEvent(FlowEvent):
    def apply(self, ctx : ActionContext):
        next_turn = ctx.state.next_turns[0]
        fraction = next_turn[Turn.FRACTION]

        ctx.state.next_turns.pop(0)
        ctx.state.next_turns.append({
            Turn.FRACTION : fraction, 
            Turn.TYPE : Turn.Type.STANDARD
        })