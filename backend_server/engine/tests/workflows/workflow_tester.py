from main.workflows.data import  WorkflowInstance
from main.workflows.factory import WorkflowFactory
from copy import deepcopy
from .scenarios.data import Scenario
from .fakes import FakeContext

class WorkflowTester:
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

            before = deepcopy(ctx.workflow_data)
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

            # print("after step exe data state")
            # print(ctx.workflow_data)

            expected_data = before
            for key, value in step_case.data_delta.items():
                setattr(expected_data, key, value);
            
            # print(f"expected data\n{expected_data}")
            # assert ctx.workflow_data == expected_data

            ctx.workflow_instance.current_step_index += 1