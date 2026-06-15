from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig
from main.workflows.step_builders import BoardSelectionMixin
from main.workflows.providers.healers import HealersProvider

from main.systems.healing import HealingSystem
from main.rules.ability.heal import HealRules

from main.state.context import ActionContext
from main.events.workflow import PopWorkflow
from main.events.flow import ChangeActiveFactionEvent

class HealersWorkflow(Workflow[HealersProvider], BoardSelectionMixin):
    def __init__(self, config : WorkflowConfig):
        super().__init__(HealersProvider())
        self.faction = config.faction
        self.system = HealingSystem()
        self.rules = HealRules()

    def set_faction(self, ctx : ActionContext):
        return [
            ChangeActiveFactionEvent(self.faction)
        ]

    def check_end_workflow(self, ctx : ActionContext) -> bool:
        return self.rules.is_finished(ctx.board, ctx.faction)

    @staticmethod
    def break_workflow_check(ctx : ActionContext):
        return ctx.workflow_data.decision

    def resolve(self, ctx : ActionContext):
        return [self.system.resolve(
            ctx.workflow_data.unit_pos, 
            ctx.workflow_data.target_pos
        )]

    def can_skip_continue_decision_step(self, ctx : ActionContext):
        return not self.rules.can_end(ctx.board, ctx.faction)

    def resolve_end_wf(self, ctx : ActionContext):
        return [ChangeActiveFactionEvent(ctx.state.turn_faction)]

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.set_faction,
                self.clear_wf_data,
            ),
            self.build_check_workflow_break_step(
                predicate_func=self.check_end_workflow,
                finish_func=self.resolve_end_wf,
            ),

            self.build_input_step(
                can_skip=self.can_skip_continue_decision_step,
                message="Do you want to finish healing?",
            ),
            self.build_check_workflow_break_step(
                predicate_func=self.break_workflow_check,
                finish_func=self.resolve_end_wf,
            ),
            self.build_target_step(message="Select a unit to heal.", snapshot=True),
            self.build_source_step(message="Select a healer."),
            self.build_resolve_step(self.resolve),
            self.build_repeat_step(index=0),
        ]
