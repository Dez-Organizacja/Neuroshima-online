from random import shuffle
from main.state.contex import ActionContext
from main.workflows.factory import WorkflowFactory
from main.engine.resolver import Resolver
from main.rules.validator import FormatValidator
from main.actions.available.core import AvailableActions
from main.systems.passive_system import PassiveSystem

class GameEngine:

    def __init__(
        self,
        passive_system,
        resolver : Resolver,
        validator : FormatValidator,
        available_actions : AvailableActions
    ):
        self.validator          : FormatValidator = validator
        self.available_actions  : AvailableActions = available_actions
        self.resolver           : Resolver = resolver
        self.passive_system     : PassiveSystem = passive_system

    def get_current_step(self, ctx : ActionContext) -> Step:
        wf = WorkflowFactory.create(ctx.workflow_instance.name)
        while(wf.finished):
            ctx.state.workflow_stack.pop()
            wf = WorkflowFactory.create(ctx.workflow_instance.name)
        return wf.get_current_step(ctx)

    def handle_action(self, ctx : ActionContext, action):
        if not self.validator.is_valid_action(ctx, action):
            raise ValueError("invalid action")
        
        input_consume = False
        wf = WorkflowFactory.create(ctx.workflow_instance.name)
        step = wf.get_current_step(ctx)
        result = step.execute(ctx, action)
        if result:
            self.resolver.resolve(ctx, result)
        # if not self.rules.can_execute_action(ctx, action):
        #     return False

        result = self.actions.execute_action(ctx, action)
        self.resolver.resolve(ctx, result)

        result = ctx.workflow.advance(ctx)
        self.resolver.resolve(ctx, result)

        self.passive_system.compute(ctx)
        return self.available_actions.get_available_actions(ctx)


    def _setup_players(self, ctx : ActionContext):
        shuffle(ctx.state.fractions)
        ctx.fraction = ctx.state.fractions[0]
        for fraction in ctx.state.fractions:
            ctx.state.add_player(fraction)

    def _setup_turn_order(self, ctx : ActionContext):
        for fraction in ctx.state.fractions:
            ctx.state.next_turns.append(
                {Turn.FRACTION : fraction, 
                 Turn.TYPE : Turn.Type.HQ_PLACEMENT}
            )

    def _set_initial_phase(self, ctx : ActionContext):
        ctx.state.phase = Phase.GAME

    def start_game(self, ctx : ActionContext):
        self._setup_players(ctx)
        self._setup_turn_order(ctx)
        self._set_initial_phase(ctx)
        self.flow_engine.start_turn(ctx)
        
        self.passive_system.compute(ctx)
        return self.available_actions.get_available_actions()
