from main.workflows.data import WorkflowData, WorkflowConfig, WorkflowName
from workflow_tester import StepCase, Scenario, FakeContext, SetupFn
from main.input.data import UserAction
from main.steps.data import StepResult
from main.events.data import ExecutionResult

class ScenarioBuilder:
    def __init__(self, 
                 name : WorkflowName, 
                 config : WorkflowConfig | None = None
        ):
        self.workflow_name = name
        self.workflow_config = config
        self.steps : list[StepCase] = []
        self._current_step : StepCase | None = None

    def when(self, action : UserAction):
        self._current_step = StepCase(action=action)
        self.steps.append(self._current_step)
        return self


    def given(self, fn : SetupFn):
        self._require_step()
        self._current_step.setup = fn
        return self

    def then_data(self, **fileds):
        self._require_step()
        self._current_step.expected_data = WorkflowData(**fileds)
        return self
    
    # def then_data_delta(self, **kwargs):
    #     self._require_step()
    #     self._current_step.expected_data = WorkflowData()


    def then_execution(self, *, 
                       effects = None, 
                       flow_events = None, 
                       workflows = None, 
                       advance = True
        ):
        self._require_step()
        self._current_step.expected_result=StepResult(
            execution_result=ExecutionResult(
                effects=effects or [], 
                flow_events = flow_events or [],
                workflow_effects=workflows or []
            ),
            advance=advance
        )
        return self

    def _require_step(self):
        if self._current_step is None:
            raise RuntimeError("Call when() first")

    def build(self):
        return Scenario(
            name= self.workflow_name,
            config= self.workflow_config,
            steps = self.steps
        )