from random import shuffle
from main.state.contex import ActionContext
from main.workflows.factory import WorkflowFactory
from main.engine.resolver import Resolver
from main.events.data import ExecutionResult
from main.events.workflow import PushWorkflow
from main.workflows.data import WorkflowConfig, WorkflowName
from main.tokens.pile_factory import PileFactory
from main.steps.step import Step
from main.input.data import UserAction

class GameEngine:

    def __init__(
        self,
        resolver : Resolver,
    ):
        self.resolver : Resolver = resolver

    @staticmethod
    def _get_step(ctx : ActionContext) -> Step:
        # print(ctx.print_wf_stack())
        wf = WorkflowFactory.create(ctx.workflow_instance)
        wf.build_steps()
        if ctx.workflow_instance.current_step_index is None:
            wf.start(ctx)
        return wf.get_current_step(ctx)
    
    def execute_step(
            self, 
            ctx : ActionContext, 
            step : Step, 
            action : UserAction | None = None
        ):
        # print("executing step", step)
        if action:
            result = step.execute(ctx, action)
        else:
            result = step.execute(ctx)
        self.resolver.resolve(ctx, result)

    def run_until_input_required(self, ctx : ActionContext):
        while True:
            step = self._get_step(ctx)
            # print(f"current_step {step}")
            if step.requires_input:
                break

            self.execute_step(ctx=ctx, step=step)

    def execute_action(self, ctx : ActionContext, action : UserAction):
        # print(f"executing action {action}")
        self.execute_step(ctx, step=self._get_step(ctx), action=action)
        self.run_until_input_required(ctx)

    def _setup_players(self, ctx : ActionContext):
        for faction in ctx.state.factions:
            ctx.state.add_player(faction)
            ctx.state.players[faction].pile = PileFactory.create_pile(faction)

    def _setup_turn_order(self, ctx : ActionContext):
        shuffle(ctx.state.factions)

    def _create_game_workflow(self, ctx : ActionContext):
        config = WorkflowConfig(factions=ctx.state.factions)
        effect = PushWorkflow(name = WorkflowName.GAME, config=config)
        result = ExecutionResult(workflow_effects=[effect])
        self.resolver.excute(ctx, result)

    def start_game(self, ctx : ActionContext):
        self._setup_players(ctx)
        self._setup_turn_order(ctx)
        self._create_game_workflow(ctx)
        self.run_until_input_required(ctx)