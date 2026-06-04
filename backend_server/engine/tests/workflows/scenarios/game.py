from main.workflows.data import WorkflowName, WorkflowConfig
from main.events.workflow import PushWorkflow, GoToStep
from .builder import ScenarioBuilder
from .registry import register

name = WorkflowName.GAME
@register(name)
def game_scenario():
    def turn_execution(faction : str):
        return PushWorkflow(
                name=WorkflowName.TURN,
                config=WorkflowConfig(faction=faction)
            )
    
    return (
        ScenarioBuilder(name, config=WorkflowConfig(factions=["moloch", "borgo"]))
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
            events=[GoToStep(index=0)],
            advance=False
        )
        
    ).build()