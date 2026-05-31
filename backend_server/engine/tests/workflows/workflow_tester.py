from main.workflows.data import  WorkflowInstance
from main.workflows.factory import WorkflowFactory
from copy import deepcopy
from .scenarios.data import Scenario, StepCase
from .fakes import FakeContext
from main.state.serialization import Serializator

class WorkflowTester:
    def get_expected_ctx(self, before : FakeContext, step_case : StepCase) -> FakeContext:
        expected_ctx = before
        for key, value in step_case.data_delta.items():
            # print(f"changing value of key {key} to {value}")
            setattr(expected_ctx.workflow_data, key, value)

        if step_case.faction_delta is not None:
            # print("nie None")
            expected_ctx.faction = step_case.faction_delta
        # print(expected_ctx)
        # print("getting exp ctx finished")
        return Serializator.to_dict_dataclass(expected_ctx)

    def run(self, scenario: Scenario):
        ctx = FakeContext(
            workflow_instance=WorkflowInstance(
                name=scenario.name,
                current_step_index= scenario.current_step,
                config=scenario.config,
            )
        )

        workflow = WorkflowFactory.create(ctx.workflow_instance)
        workflow.build_steps()

        for step_case in scenario.steps:
            print("######################")
            print("procesing step")
            print(step_case)
            print("------------")

            if step_case.setup:
                step_case.setup(ctx)

            before = deepcopy(ctx)
            # print(f"before step exe data state")
            # print(before)

            step = workflow.get_current_step(ctx)

            print("START EXECUTING")
            if step_case.action:
                result = step.execute(ctx, step_case.action)
            else:
                print("WITHOUT ACTION")
                result = step.execute(ctx)
                
            print("END EXECUTING")
            print("after step exe result")
            print(result)

            print(f"expected result")
            print(step_case.expected_result)

            assert result == step_case.expected_result

            print("after step exe state")
            print(Serializator.to_dict_dataclass(ctx))

            expected_ctx = self.get_expected_ctx(before, step_case)
            print(f"expected ctx\n{expected_ctx}")
            
            assert Serializator.to_dict_dataclass(ctx) == expected_ctx

            ctx.workflow_instance.current_step_index += 1