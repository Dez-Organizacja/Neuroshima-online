from abc import ABC, abstractmethod
from main.state.contex import ActionContext
from main.utils.variable import Turn, Phase

class Event(ABC):
    @abstractmethod
    def apply(self, ctx : ActionContext):
        pass