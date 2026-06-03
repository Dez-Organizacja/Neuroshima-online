from .registry import ScenarioRegistry
from .executer import ScenarioExecuter
import pytest

@pytest.mark.parametrize("name, scenario_func", ScenarioRegistry.all_scenarios())
def test_scenario(name, scenario_func):
    scenario = scenario_func()
    assert scenario is not None
    ScenarioExecuter().run(scenario)