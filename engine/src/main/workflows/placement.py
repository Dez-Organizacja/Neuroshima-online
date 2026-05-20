from main.workflows.base import Workflow
from main.rules.workflow.placement import PlaceRules
from main.workflows.step_builders import BoardSelectionMixin
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.events.effects import PlaceEffect
from main.actions.execute.result import ActionResult
from main.steps.config import ResolveStepConfig

class PlaceWorkflow(BoardSelectionMixin, Workflow[PlaceRules]):
    def __int__(self):
        super().__init__(rules=PlaceRules())

    def resolve_function(self, ctx : ActionContext):
        unit = ctx.player.hand.get_token(ctx.workflow_data.slot)
        return ActionResult(effects=[
            PlaceEffect(
                pos = ctx.workflow_data.unit_pos,
                unit=unit,
            )
        ])

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.resolve_function,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_input_steps(setter=WorkflowData.set_unit_pos),
            self.build_end_step()            
        ]