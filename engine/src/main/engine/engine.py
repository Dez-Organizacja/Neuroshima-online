from random import shuffle
from main.state.contex import ActionContext
from main.workflows.factory import WorkflowFactory
from main.engine.resolver import Resolver
from main.rules.validator import FormatValidator
from main.actions.available.core import AvailableActions
from main.events.data import ExecutionResult
from main.events.workflow import PushWorkflow
from main.workflows.data import GameConfig

from main.steps.data import StepResult

class GameEngine:

    def __init__(
        self,
        resolver : Resolver,
        available_actions : AvailableActions
    ):
        self.available_actions  : AvailableActions = available_actions
        self.resolver           : Resolver = resolver

    def execute_action(self, ctx : ActionContext, action):

        input_consumed = False
        while True:
            wf = WorkflowFactory.create(ctx.workflow_instance.config)
            step = wf.get_current_step(ctx)
            
            if step.requires_input and input_consumed:
                break
        
            result = step.execute(ctx, action)
            self.resolver.resolve(ctx, result)
            
            if result.input_consumed:
                input_consumed = True

    def _setup_players(self, ctx : ActionContext):
        for fraction in ctx.state.fractions:
            ctx.state.add_player(fraction)

    def _setup_turn_order(self, ctx : ActionContext):
        shuffle(ctx.state.fractions)

    def _create_game_workflow(self, ctx : ActionContext):
        config = GameConfig(fractions=ctx.state.fractions)
        effect = PushWorkflow(config=config)
        result = ExecutionResult(workflow_effects=[effect])
        self.resolver.excute(ctx, result)

    def start_game(self, ctx : ActionContext):
        self._setup_players(ctx)
        self._setup_turn_order(ctx)
        self._create_game_workflow(ctx)