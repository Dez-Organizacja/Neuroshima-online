from main.state.contex import ActionContext
from main.workflows.base import Workflow
from main.rules.workflow.push import PushRules
from main.utils.variable import Bottom
from main.steps.config import InputStepConfig, ResolveStepConfig
from main.state.user_action import BoardAction
from main.workflows.data import WorkflowData, WorkflowName
from main.effects.board_effects import MoveEffect
from main.actions.exeute_actions.action_result import ActionResult

class PushWorkflow(Workflow):
    def __init__(self):
        super().__init__(rules=PushRules())


    def build_source_step(self):
        return InputStepConfig[BoardAction](
            getter=BoardAction.get_pos,
            setter=WorkflowData.set_unit_pos,
            get_bottoms=self.rules.get_available_bottoms,
            get_positions=self.rules.get_sources
        )

    def build_target_step(self):
        return InputStepConfig[BoardAction](
            getter=BoardAction.get_pos,
            setter=WorkflowData.set_target_pos,
            get_bottoms=self.rules.get_available_bottoms,
            get_positions=self.rules.get_targets
        )

    def build_destination_step(self):
        return InputStepConfig[BoardAction](
            getter=BoardAction.get_pos,
            setter=WorkflowData.set_destination,
            get_positions=self.rules.get_destinations
        )

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.resolve_push,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_source_step(),
            self.build_target_step(),
            self.build_destination_step(),
            self.build_end_step()
        ]

    @staticmethod
    def resolve_push(ctx : ActionContext):
        move = MoveEffect(
            from_pos=ctx.workflow_data.target_pos,
            to_pos=ctx.workflow_data.destination
        )
        return ActionResult(effects=[move])

    @classmethod
    def get_first_step_index(cls, source : WorkflowName):
        return 1 if source == WorkflowName.BOARD else 0