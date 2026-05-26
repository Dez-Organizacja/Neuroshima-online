from main.steps.data import StepResult
from main.state.serialization import Serializator
from dataclasses import dataclass, field
from typing import Callable
from main.workflows.data import (
    WorkflowData, 
    WorkflowInstance, 
    WorkflowName,
    WorkflowConfig
)
from main.workflows.factory import WorkflowFactory
from main.input.data import UserAction
from copy import deepcopy

@dataclass
class FakeContext:
    workflow_instance : WorkflowInstance
    workflow_data : WorkflowData = field(default_factory=WorkflowData)

@dataclass
class StepCase:
    expected_result : StepResult = field(default_factory=StepResult)
    expected_data : WorkflowData | None = None
    action : UserAction | None = None
    setup : Callable[[WorkflowData]] | None = None


@dataclass
class Scenario:
    name : WorkflowName
    steps : list[StepCase]

    current_step : int = 0
    config : WorkflowConfig = field(default_factory=WorkflowConfig)


class WokrflowTester:
    def run(self, scenario: Scenario):
        ctx = FakeContext(
            workflow_instance=WorkflowInstance(
                name=scenario.name,
                current_step_index=scenario.current_step,
                config=scenario.config,
            )
        )

        workflow = WorkflowFactory.create(ctx.workflow_instance)
        workflow.build_steps()

        for step_case in scenario.steps:
            if step_case.setup:
                step_case.setup(ctx.workflow_data)

            before = deepcopy(ctx.workflow_data)

            step = workflow.get_current_step(ctx)

            if step_case.action:
                result = step.execute(ctx, step_case.action)
            else:
                result = step.execute(ctx)

            assert result == step_case.expected_result

            expected_data = step_case.expected_data or before
            assert ctx.workflow_data == expected_data

            ctx.workflow_instance.current_step_index += 1