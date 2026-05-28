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
from main.tokens.hand import Hand
from copy import deepcopy

@dataclass
class FakePlayerState:
    hand : Hand = field(default_factory=Hand)

@dataclass
class FakeContext:
    workflow_instance : WorkflowInstance
    workflow_data : WorkflowData = field(default_factory=WorkflowData)
    player : FakePlayerState = field(default_factory=FakePlayerState)
    faction : str = "moloch"

SetupFn = Callable[[FakeContext], None]

@dataclass
class StepCase:
    expected_result : StepResult = field(default_factory=StepResult)
    # data_delta : WorkflowData | None = None
    expected_data : WorkflowData | None = None
    action : UserAction | None = None
    setup : SetupFn | None = None


@dataclass
class Scenario:
    name : WorkflowName
    steps : list[StepCase]

    current_step : int = 0
    config : WorkflowConfig = field(default_factory=WorkflowConfig)


class WorkflowTester:
    # def merge_workflow_data(data : WorkflowData, new_data : WorkflowData):
    #     d = {

    #     }

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
            print("######################")
            print("procesing step")
            print(step_case)
            print("######################")

            if step_case.setup:
                step_case.setup(ctx)

            before = deepcopy(ctx.workflow_data)
            print(f"before step exe data state")
            print(before)

            step = workflow.get_current_step(ctx)

            if step_case.action:
                result = step.execute(ctx, step_case.action)
            else:
                result = step.execute(ctx)

            print("after step exe result")
            print(f"result {result}")

            assert result == step_case.expected_result

            print("after step exe data state")
            print(ctx.workflow_data)

            expected_data = step_case.expected_data or before
            print(f"expected data{expected_data}"   )
            assert ctx.workflow_data == expected_data

            ctx.workflow_instance.current_step_index += 1