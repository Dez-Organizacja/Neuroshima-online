from main.workflows.base import Workflow
from main.rules.push import PushRules
from main.utils.variable import Bottom
from main.steps.config import StepConfig
from main.state.contex import ActionContext
from main.state.user_action import BoardAction
from main.workflows.data import WorkflowData, WorkflowSource, WorkflowName
from main.actions.exeute_actions.action_result import ActionResult
from main.effects.board_effects import DiscardActiveTokenEffect, MoveEffect
from main.effects.flow_effects import StartWorkflow

class PushWorkflow(Workflow):
    def __init__(self):
        super().__init__(rules=PushRules())


    def build_source_step(self):
        return StepConfig[BoardAction](
            getter=BoardAction.get_pos,
            setter=WorkflowData.unit_pos,
            allowed_bottoms=[Bottom.CANCEL, Bottom.DISCARD],
            get_positions=self.get_sources
        )

    def build_target_step(self):
        return StepConfig[BoardAction](
            getter=BoardAction.get_pos,
            setter=WorkflowData.target_pos,
            allowed_bottoms=[Bottom.CANCEL],
            get_positions=self.get_targets
        )

    def build_destination_step(self):
        return StepConfig[BoardAction](
            getter=BoardAction.get_pos,
            setter=WorkflowData.destination,
            get_positions=self.get_destinations
        )

    def build_steps(self):
        return [
            self.build_source_step(),
            self.build_target_step(),
            self.build_destination_step(),
        ]
    
    def finish(self, ctx : ActionContext):
        push = MoveEffect(
            from_pos=ctx.workflow_data.target_pos,
            to_pos=ctx.workflow_data.destination
        )
        result = ActionResult(
            effects=[push],
            flow_events=[StartWorkflow(WorkflowName.CHOOSING_ACTION)]
        )
        if ctx.workflow_data.source == WorkflowSource.HAND:
            result.effects.append(DiscardActiveTokenEffect())
        
        return result