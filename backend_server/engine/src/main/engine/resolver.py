from main.events.data import ExecutionResult, Event
from main.state.contex import ActionContext
from main.steps.data import StepResult
from main.systems.passive_systems import PassiveSystems

class Resolver():
    def apply(self, ctx : ActionContext, events : list[Event]):
        dirty = False
        for event in events:
            event.apply(ctx)
            if event.recompute_passive:
                dirty = True

        if dirty:
            PassiveSystems.compute(ctx)

    def excute(self, ctx : ActionContext, result : ExecutionResult):
        self.apply(ctx, result.effects)

        ctx.state.flow_queue.extend(result.flow_events)
        while ctx.state.flow_queue:
            event = ctx.state.flow_queue.popleft()
            new_result : ExecutionResult = event.apply(ctx)
            if new_result:
                self.excute(ctx, new_result)
        
        self.apply(ctx, result.workflow_effects)

    def resolve(self, ctx : ActionContext, result : StepResult):
        # print(f"resolving step result {result}")
        if result.advance:
            ctx.workflow_instance.current_step_index += 1
            
        self.excute(ctx, result.execution_result)