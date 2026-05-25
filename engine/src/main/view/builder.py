from main.state.contex import ActionContext
from main.view.state import StateViewBuilder
from main.view.step import StepViewBuilder

class GameViewBuilder:
    def __init__(self):
        self.state_view = StateViewBuilder()
        self.step_view = StepViewBuilder()

    def build(self, ctx : ActionContext) -> dict:
        # print("cos", cos)
        return {
            "state" : self.state_view.build(ctx),
            **self.step_view.build_step(ctx).to_dict()
        }