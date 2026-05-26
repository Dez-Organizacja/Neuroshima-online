from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Event(ABC):
    recompute_passive = False
    @abstractmethod
    def apply(self, ctx):
        pass

class Effect(Event, ABC):
    pass

class FlowEvent(Event, ABC):
    pass

class WorkflowEvent(Event, ABC):
    pass

@dataclass
class ExecutionResult:
    effects : list[Effect] = field(default_factory=list)
    flow_events : list[FlowEvent] = field(default_factory=list)
    workflow_effects : list[WorkflowEvent] = field(default_factory=list)

    def print(self):
        print("flows")
        for flow in self.flow_events:
            print(type(flow).__name__)
        
        print("workflow_events")
        for wf_event in self.workflow_effects:
            print(type(wf_event).__name__)

        print("--------------------")