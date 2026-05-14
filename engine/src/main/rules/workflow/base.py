from main.state.contex import ActionContext
from abc import ABC

class WorkflowRules(ABC):

    @staticmethod
    def get_available_tokens(ctx : ActionContext):
        return {}
    
    @staticmethod
    def get_available_bottoms(ctx : ActionContext):
        return []
    
    @staticmethod
    def get_sources(ctx : ActionContext):
        return []
    
    @staticmethod
    def get_targets(ctx : ActionContext):
        return []

    @staticmethod
    def get_destinations(ctx : ActionContext):
        return []