from main.workflows.data import WorkflowData, WorkflowConfig, WorkflowName
from .data import StepCase, Scenario, SetupFn
from main.input.data import UserAction
from main.steps.data import StepResult
from main.events.data import Event
from main.state.contex import ActionContext


class ScenarioBuilder:
    def __init__(self, 
                 name : WorkflowName, 
                 config : WorkflowConfig | None = None,
                 factions : list[str] | None = None,
        ):
        self.factions = factions or ["moloch", "borgo"]
        self.workflow_name = name
        self.workflow_config = config or WorkflowConfig()
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
    
    @staticmethod
    def mark_onclick_consumed(ctx : ActionContext):
        ctx.workflow_instance.on_click_consumed = True

    def given_wf_onclick_consumed(self):
        return self.given(self.mark_onclick_consumed)

    def then_data_delta(self, **kwargs):
        self._require_step()
        for key in kwargs:
            if not hasattr(WorkflowData, key):
                raise RuntimeError(f"data has not argument {key}")
        self._current_step.data_delta = kwargs
        return self

    def then_faction(self, faction, turn : bool = False):
        self._require_step()
        if turn:
            self._current_step.turn_faction_delta = faction
        self._current_step.faction_delta = faction
        return self

    def then_execution(self, *, 
                       events : list[Event],
                       advance = True
        ):
        self._require_step()
        self._current_step.expected_result=StepResult(
            execution_result=events,
            advance=advance
        )
        return self

    def tick(self):
        return self.when(None)

    def _require_step(self):
        if self._current_step is None:
            raise RuntimeError("Call when() first")

    def build(self):
        return Scenario(
            factions=self.factions,
            name= self.workflow_name,
            config= self.workflow_config,
            steps = self.steps,
        )