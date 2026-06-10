from main.events.data import Event
from main.state.contex import ActionContext
from main.steps.data import StepResult
from main.systems.passive_systems import PassiveSystems

class Resolver():
    def execute(self, ctx : ActionContext, result : list[Event]):
        dirty = False
        ctx.state.events_queue.extend(result)
        while ctx.state.events_queue:
            event = ctx.state.events_queue.popleft()
            if event.recompute_passive:
                dirty = True    

            result = event.apply(ctx) or []
            ctx.state.events_queue.extend(result)

        if dirty:
            PassiveSystems.compute(ctx.board)
    
    def resolve(self, ctx : ActionContext, result : StepResult):
        # print(f"resolving step result {result}")
        if result.advance:
            ctx.workflow_instance.current_step_index += 1
            
        self.execute(ctx, result.execution_result)