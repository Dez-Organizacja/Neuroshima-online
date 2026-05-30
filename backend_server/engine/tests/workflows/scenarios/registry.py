from .data import Scenario
from typing import Callable
from main.workflows.data import WorkflowName
from collections import defaultdict

scenario_builder = Callable[[], Scenario]
SCENARIOS_REGISTRY : dict[WorkflowName, list[scenario_builder]] = defaultdict(list)

def register(name : WorkflowName):
    def wrapper(func : scenario_builder):
        SCENARIOS_REGISTRY[name].append(func)
        return func
    return wrapper

def iter_scenarios() -> list[scenario_builder]:
    return [
        builder
        for builders in SCENARIOS_REGISTRY.values() 
        for builder in builders
    ]