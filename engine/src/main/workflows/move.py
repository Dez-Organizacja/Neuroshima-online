from main.actions.exeute_actions.action_result import ActionResult
from main.effects.board_effects import MoveEffect
from main.state.contex import ActionContext
from main.workflows.base import Workflow
from main.workflows.data import WorkflowData, WorkflowName
from main.rules.workflow.move import MoveRules
from main.steps.config import InputStepConfig, ResolveStepConfig
from main.state.user_action import BoardAction

class MoveWorkflow(Workflow):
    def __init__(self):
        super().__init__(rules=MoveRules())

    def build_source_step(self):
        return InputStepConfig[BoardAction](
                getter=BoardAction.get_pos,
                setter=WorkflowData.set_unit_pos,
                get_bottoms=self.rules.get_available_bottoms,
                get_positions=self.rules.get_sources
            ), 

    def build_destination_step(self):
        return InputStepConfig[BoardAction](
                getter=BoardAction.get_pos,
                setter=WorkflowData.set_destination,
                get_bottoms=self.rules.get_available_bottoms,
                get_positions=self.rules.get_destinations
            )

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.resolve_move,
            wf_finished=True
        )

    def build_steps(self):
        return [
            self.build_source_step(),
            self.build_destination_step(),
            self.build_end_step()
        ]

    @staticmethod
    def resolve_move(ctx : ActionContext):
        move = MoveEffect(
            from_pos=ctx.workflow_data.unit_pos,
            to_pos=ctx.workflow_data.destination
        )
        return ActionResult(effects=[move])


    def get_first_step_index(cls, source : WorkflowName):
        return 1 if source == WorkflowName.BOARD else 0