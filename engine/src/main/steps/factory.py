from main.steps.config import StepConfig, StepName
from main.steps.step import (
    ResolveStep,
    InitStep,
    WaitingStep,
    SetStep,
    RepeatStep,
    Step
)

class StepFactory:
    REGISTRY = {
        StepName.RESOLVE : ResolveStep,
        StepName.INIT : InitStep,
        StepName.WAITING : WaitingStep,
        StepName.SET : SetStep,
        StepName.REPEAT : RepeatStep
    }
    def __init__(self):
        pass

    @classmethod
    def create(cls, config : StepConfig) -> Step[StepConfig]:
        step_class = cls.REGISTRY.get(config.name)
        if not step_class:
            raise ValueError(f"Unknown step type: {config.name}")
        return step_class(config)
