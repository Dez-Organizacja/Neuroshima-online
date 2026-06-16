from main.events.data import Event
from main.state.context import ActionContext
from main.steps.data import StepResult
from main.systems.passive_systems import PassiveSystems
from main.workflows.data import WorkflowName

class Resolver():
    @staticmethod
    def _commit_pending_workflow(ctx : ActionContext):
        print("TRYING TO COMMIT PENDING WORKFLOW")
        if not ctx.state.pending_workflows:
            return
        
        print(ctx.workflow_instance)
        if ctx.workflow_instance.name != WorkflowName.GAME:
            return

        print("commiting pending workflow")
        print(f"pending workflow {ctx.state.pending_workflows}")
        ctx.state.workflow_stack[-1] = ctx.state.pending_workflows[-1]
        ctx.state.pending_workflows.pop()

    def execute(self, ctx : ActionContext, result : list[Event]):
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

        self._commit_pending_workflow(ctx)
    
    @staticmethod
    def advance(ctx : ActionContext):
        ctx.workflow_instance.current_step_index += 1

    def resolve(self, ctx : ActionContext, result : StepResult):
        # print(f"resolving step result {result}")
        if result.advance:
            self.advance(ctx)
            
        self.execute(ctx, result.execution_result)
