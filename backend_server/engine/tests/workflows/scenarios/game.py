from main.workflows.data import WorkflowName, WorkflowConfig
from main.events.workflow import PushWorkflow, GoToStep
from .builder import ScenarioBuilder
from .registry import register

name = WorkflowName.GAME
@register(name)
def game_scenario():
    def turn_execution(faction : str, hand_limit : int = 3):
        return PushWorkflow(
                name=WorkflowName.TURN,
                config=WorkflowConfig(faction=faction, hand_limit=hand_limit)
            )

    def headquarter_execution(faction : str):
        return PushWorkflow(
                name=WorkflowName.HEADQUARTER_TURN,
                config=WorkflowConfig(faction=faction)
            )
    
    return (
        ScenarioBuilder(name, config=WorkflowConfig(factions=["moloch", "borgo"]))
        .tick()
        .then_execution(
            events=[headquarter_execution("moloch")]
        )

        .tick()
        .then_execution(
            events=[headquarter_execution("borgo")]
        )

        .tick()
        .then_execution(
            events=[turn_execution("moloch", hand_limit=1)]
        )

        .tick()
        .then_execution(
            events=[turn_execution("borgo", hand_limit=2)]
        )

        .tick()
        .then_execution(
            events=[turn_execution("moloch")]
        )

        .tick()
        .then_execution(
            events=[turn_execution("borgo")]
        )

        .tick()
        .then_execution(
            events=[GoToStep(index=4)],
            advance=False
        )
        
    ).build()
