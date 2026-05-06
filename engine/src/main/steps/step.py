from main.state.contex import ActionContext
from main.actions.available_actions.available_action_result import AvailableActionResult
from main.state.user_action import UserAction
from main.steps.config import StepConfig

class Step:
    def __init__(self, config : StepConfig):
        self.config : StepConfig = config

    def execute(self, action : UserAction, ctx : ActionContext):
        value = self.config.getter(action)
        self.config.setter(ctx.workflow_data, value)

    def get_available_actions(self, ctx : ActionContext):
        return AvailableActionResult(
            positions= self.config.get_positions(ctx),
            bottoms=self.config.allowed_bottoms,
            hand=self.config.get_available_tokens(ctx)
        )

# class ChooseSourceStep(Step):
#     def __init__(self, workflow_rules):
#         super().__init__()
#         self.workflow_rules = workflow_rules

#     def execute(self, action : UserAction, ctx : ActionContext):
#         ctx.workflow_data.unit_pos = action.pos
    
#     def get_available_actions(self, ctx):
#         return AvailableActionResult(
#             positions=self.workflow_rules.get_available_sources(ctx),
#             bottoms=ctx.workflow.get_allowed_bottoms(ctx)
#         )
    
# class ChooseDestinationStep(Step):
#     def __init__(self, workflow_rules):
#         super().__init__()
#         self.workflow_rules = workflow_rules

#     def execute(self, action : UserAction, ctx : ActionContext):
#         ctx.workflow_data.destination = action.pos
    
#     def get_available_actions(self, ctx):
#         return AvailableActionResult(
#             positions=self.workflow_rules.get_available_destinations(ctx),
#             bottoms=ctx.workflow.get_allowed_bottoms(ctx)
#         )