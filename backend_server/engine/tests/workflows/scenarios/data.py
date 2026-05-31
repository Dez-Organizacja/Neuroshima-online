from dataclasses import dataclass, field
from main.steps.data import StepResult
from main.input.data import UserAction
from main.workflows.data import WorkflowName, WorkflowConfig
from typing import Callable
from ..fakes import FakeContext

SetupFn = Callable[[FakeContext], None]

@dataclass
class StepCase:
    expected_result : StepResult = field(default_factory=StepResult)
    data_delta : dict = field(default_factory=dict)
    faction_delta : str | None = None
    # expected_data : WorkflowData | None = None
    action : UserAction | None = None
    setup : SetupFn | None = None


@dataclass
class Scenario:
    name : WorkflowName
    steps : list[StepCase]
    
    current_step : int = 0
    config : WorkflowConfig = field(default_factory=WorkflowConfig)