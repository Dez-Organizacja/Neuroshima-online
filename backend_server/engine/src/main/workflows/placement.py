from main.workflows.base import Workflow
from main.workflows.providers.placement import PlacementProvider
from main.workflows.step_builders import BoardSelectionMixin
from main.state.context import ActionContext
from main.workflows.data import WorkflowName
from main.events.workflow import PushWorkflow
from main.events.effects import ClearSelectedHandSlotEffect, DiscardTokenEffect, PlaceEffect
from main.events.data import Event

class PlaceWorkflow(Workflow[PlacementProvider], BoardSelectionMixin):
    def __init__(self):
        super().__init__(action_provider=PlacementProvider())

    def resolve_function(self, ctx : ActionContext) -> list[Event]:
        return [
                PlaceEffect(
                    pos = ctx.workflow_data.unit_pos,
                    name = ctx.player.hand.get(ctx.workflow_data.slot),
                    faction = ctx.faction
                ),
                DiscardTokenEffect(ctx.workflow_data.slot),
                ClearSelectedHandSlotEffect(),
                PushWorkflow(name=WorkflowName.ROTATE)
            ]
    
    def _build_steps(self):
        return [
            self.build_source_step(message="Select a field for the token."),
            self.build_resolve_step(self.resolve_function),
            self.build_end_step()
        ]