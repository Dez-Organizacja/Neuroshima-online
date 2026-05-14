from main.rules.workflow.base import WorkflowRules
from abc import ABC, abstractmethod

class TargetWorkflowRules(ABC, WorkflowRules):
    @abstractmethod
    def get_available_targets(self, ctx):
        pass

    @abstractmethod
    def get_available_bottoms(self, ctx):
        pass