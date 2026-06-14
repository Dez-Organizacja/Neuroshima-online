from main.workflows.base import Workflow

class GameOverWorkflow(Workflow):
    def __init__(self):
        super().__init__()

    def _build_steps(self):
        return [
            self.build_input_step(),
            self.build_repeat_step(index=0),
        ]