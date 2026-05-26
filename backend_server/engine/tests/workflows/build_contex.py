from main.state.contex import ActionContext
from main.state.game_state import GameState
from main.workflows.data import WorkflowName, WorkflowData, WorkflowInstance, WorkflowConfig
from main.rules.game import GameRules
from main.steps.data import StepResult
from main.engine.engine import GameEngine
from main.input.data import UserAction

def build_contex(
        data : WorkflowData,
        name : WorkflowName, 
        config : WorkflowConfig = WorkflowConfig(), 
        fractions : list[str] = ["moloch", "borgo"]
    ) -> ActionContext:
    return ActionContext(
        state=GameState(
            fractions=fractions,
            workflow_data=data,
            workflow_stack=[
                WorkflowInstance(name=name, current_step_index=0)
            ]
        ),
        rules=GameRules()
    )

def execute_step(
        ctx : ActionContext, 
        action : UserAction | None = None
    ) -> StepResult:
    step = GameEngine._get_step(ctx)
    if action:
        return step.execute(ctx, action)

    return step.execute(ctx)
