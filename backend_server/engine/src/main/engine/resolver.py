from main.events.data import Event
from main.state.context import ActionContext
from main.steps.data import StepResult
from main.systems.passive_systems import PassiveSystems
from main.workflows.data import WorkflowName

class Resolver():
    @staticmethod
    def _commit_pending_workflow(ctx : ActionContext):
        if not ctx.state.pending_workflows:
            return
        
        if ctx.workflow_instance.name != WorkflowName.GAME:
            return

        # print("commiting pending workflow")
        # print(f"pending workflow {ctx.state.pending_workflow}")
        ctx.state.workflow_stack[-1] = ctx.state.pending_workflows[-1]
        ctx.state.pending_workflows.pop()

    @staticmethod
    def execute(ctx : ActionContext, result : list[Event]):
        dirty = False
        ctx.state.events_queue.extend(result)
        while ctx.state.events_queue:
            event = ctx.state.events_queue.popleft()
            # print(f"event {event}")
            if event.recompute_passive:
                dirty = True    

            result = event.apply(ctx) or []
            # print(f"result {result}")
            ctx.state.events_queue.extend(result)

        if dirty:
            PassiveSystems.compute(ctx.board)
    
    @staticmethod
    def advance(ctx : ActionContext):
        ctx.workflow_instance.current_step_index += 1

    def resolve(self, ctx : ActionContext, result : StepResult):
        # print(f"resolving step result {result}")
        if result.advance:
            self.advance(ctx)
            
        self.execute(ctx, result.execution_result)
        self._commit_pending_workflow(ctx)