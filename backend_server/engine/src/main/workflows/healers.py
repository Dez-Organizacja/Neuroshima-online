from main.workflows.base import Workflow
from main.workflows.providers.healers import HealersProvider
from main.workflows.step_builders import BoardSelectionMixin
from main.workflows.data import HealersConfig
from main.steps.config import ResolveStepConfig, RepeatStepConfig
from main.state.contex import ActionContext
from main.events.data import ExecutionResult
from main.events.workflow import PopWorkflow
from main.events.effects import HealEffect, ClearWorkflowDataEffect

class HealersWorkflow(Workflow[HealersProvider], BoardSelectionMixin):
    def __init__(self, config : HealersConfig):
        super().__init__(HealersProvider())
        self.faction = config.faction

    def build_init_step(self):
        def func(ctx : ActionContext):
            return ExecutionResult(
                effects=[ClearWorkflowDataEffect()]
            )
        return ResolveStepConfig(resolve_func=func)

    def build_check_end_workflow_step(self):
        def func(ctx : ActionContext):
            candidates = self.action_provider.get_available_positions(
                ctx, 
                self.faction
            )
            if len(candidates) == 0:
                return ExecutionResult(workflow_effects=[PopWorkflow()])
        return ResolveStepConfig(resolve_func=func)

    def build_resolve_step(self):
        def func(ctx : ActionContext):
            heal = HealEffect(
                source_pos=ctx.workflow_data.unit_pos,
                target_pos=ctx.workflow_data.target_pos
            )
            return ExecutionResult(
                effects=[heal],
            )
            
        return ResolveStepConfig(resolve_func=func)

    def build_repeat_step(self):
        return RepeatStepConfig(repeat_from_index=1)

    def _build_steps(self):
        return [
            self.build_init_step(),
            self.build_check_end_workflow_step(),
            self.build_source_step(),
            self.build_target_step(),
            self.build_resolve_step(),
            self.build_repeat_step()
        ]