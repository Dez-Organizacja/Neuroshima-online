from .data import Scenario
from typing import Callable

class ScenarioRegistry:
    _SCENARIOS : dict[str, Callable[[], Scenario]] = {}

    @classmethod
    def register(cls, name):
        def decorator(func):
            cls._SCENARIOS[name] = func
            return func
        return decorator
    
    @classmethod
    def all_scenarios(cls):
        return cls._SCENARIOS.items()