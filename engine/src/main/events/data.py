from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from main.events.effects import Effect
from main.events.flow import FlowEvent
from main.events.workflow import WorkflowEvent
from main.state.contex import ActionContext

@dataclass
class ActionResult:
    effects : list[Effect] = field(default_factory=list)
    flow_events : list[FlowEvent] = field(default_factory=list)

@dataclass
class ExecutionResult:
    action_result : ActionResult = field(default_factory=ActionResult)
    workflow_effects : list[WorkflowEvent] = field(default_factory=list)

class Event(ABC):
    @abstractmethod
    def apply(self, ctx : ActionContext):
        pass