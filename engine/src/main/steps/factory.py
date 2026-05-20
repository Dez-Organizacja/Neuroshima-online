from main.steps.config import StepType, StepConfig
from main.steps.step import InputStep, ChooseActionStep, AutomaticStep

class StepFactory:
    REGISTRY = {
        StepType.INPUT: InputStep,
        StepType.CHOICE: ChooseActionStep,
        StepType.AUTOMATIC: AutomaticStep
    }
    def __init__(self):
        pass

    @classmethod
    def create(cls, config : StepConfig):
        step_class = cls.REGISTRY.get(config.name)
        if not step_class:
            raise ValueError(f"Unknown step type: {config.name}")
        return step_class(config)
