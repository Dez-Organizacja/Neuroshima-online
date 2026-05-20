from main.actions.execute.result import ActionResult
from main.state.contex import ActionContext

class Resolver():
    def apply(self, ctx, events):
        for event in events:
            event.apply(ctx)

    def resolve(self, ctx : ActionContext, result : ActionResult):
        self.apply(ctx, result.effects)
        self.apply(ctx, result.interaction_state_changes)

        ctx.state.flow_queue.extend(result.flow_events)
        while ctx.state.flow_queue:
            event = ctx.state.flow_queue.popleft()
            result = event.apply(ctx)
            if result:
                self.resolve(ctx, result)
                