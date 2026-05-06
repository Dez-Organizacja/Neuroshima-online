from main.workflows.base import Workflow
from main.workflows.data import WorkflowData
from main.workflows.data import WorkflowSource
from main.state.contex import ActionContext
from main.rules.move import MoveRules
from main.actions.exeute_actions.action_result import ActionResult
from main.effects.board_effects import DiscardActiveTokenEffect, MoveEffect
from main.effects.flow_effects import StartWorkflow
from main.workflows.data import WorkflowName
from main.steps.config import StepConfig
from main.state.user_action import BoardAction
from main.utils.variable import Bottom

class MoveWorkflow(Workflow):
    def __init__(self):
        super().__init__(rules=MoveRules())

    

    def build_source_step(self):
        return StepConfig[BoardAction](
                getter=BoardAction.get_pos,
                setter=WorkflowData.set_unit_pos,
                allowed_bottoms=[Bottom.CANCEL, Bottom.DISCARD],
                get_positions=self.get_sources
            ), 

    def build_destination_step(self):
        return StepConfig[BoardAction](
                getter=BoardAction.get_pos,
                setter=WorkflowData.set_destination,
                allowed_bottoms=[Bottom.CANCEL],
                get_positions=self.get_destinations
            )

    def build_steps(self):
        return [
            self.build_source_step(),
            self.build_destination_step()
        ]
    
    def finish(self, ctx):
        move = MoveEffect(
            from_pos=ctx.workflow_data.unit_pos,
            to_pos=ctx.workflow_data.destination
        )
        result = ActionResult(
            effects=[move],
            flow_events=[StartWorkflow(WorkflowName.ROTATE)],
        )
        if ctx.workflow_data.source == WorkflowSource.HAND:
            result.effects.append(DiscardActiveTokenEffect())

        return result