import pytest
from .workflow_tester import WorkflowTester
from .scenarios import iter_scenarios

@pytest.mark.parametrize(
        "scenario_builder", 
        iter_scenarios(), 
        ids=[f.__name__ for f in iter_scenarios()]        
)
def test_workflows(scenario_builder):
    scenario = scenario_builder()
#     print("scenario\n")
#     print(scenario)
    WorkflowTester().run(scenario)