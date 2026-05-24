from main.workflows.base import Workflow
from main.workflows.providers.placement import PlacementProvider
from main.workflows.step_builders import BoardSelectionMixin
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.events.effects import PlaceEffect
from main.events.data import ExecutionResult
from main.workflows.step_builders import build_end_step

class PlaceWorkflow(BoardSelectionMixin, Workflow[PlacementProvider]):
    def __int__(self):
        super().__init__(action_provider=PlacementProvider())

    def resolve_function(self, ctx : ActionContext):
        unit = ctx.player.hand.get_token(ctx.workflow_data.slot)
        return ExecutionResult(effects=[
            PlaceEffect(
                pos = ctx.workflow_data.unit_pos,
                unit=unit,
            )
        ])

    def build_steps(self):
        return [
            self.build_input_steps(setter=WorkflowData.set_unit_pos),
            build_end_step(self.resolve_function)            
        ]