from main.state.contex import ActionContext
from main.actions.exeute_actions.action_result import ActionResult
from main.effects.board_effects import DiscardActiveTokenEffect, MoveEffect
from main.workflows.data import WorkflowSource

def resolve_move(ctx : ActionContext):
    move = MoveEffect(
        from_pos=ctx.workflow_data.unit_pos,
        to_pos=ctx.workflow_data.destination
    )
    return ActionResult(effects=[move])

def resolve_push(ctx : ActionContext):
    move = MoveEffect(
        from_pos=ctx.workflow_data.target_pos,
        to_pos=ctx.workflow_data.destination
    )
    return ActionResult(effects=[move])