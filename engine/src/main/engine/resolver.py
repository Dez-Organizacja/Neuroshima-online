from main.events.data import ActionResult, ExecutionResult
from main.state.contex import ActionContext

class Resolver():
    def apply(self, ctx : ActionContext, events):
        for event in events:
            event.apply(ctx)

    def resolve(self, ctx : ActionContext, result : ExecutionResult):
        action_result : ActionResult = result.action_result
        self.apply(ctx, action_result.effects)
        self.apply(ctx, result.workflow_effects)

        ctx.state.flow_queue.extend(action_result.flow_events)
        while ctx.state.flow_queue:
            event = ctx.state.flow_queue.popleft()
            result : ExecutionResult = event.apply(ctx)
            if result:
                self.resolve(ctx, result)
                