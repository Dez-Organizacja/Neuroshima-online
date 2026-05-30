from main.workflows.data import WorkflowName, GameConfig, TurnConfig
from main.events.workflow import PushWorkflow, GoToStep
from .builder import ScenarioBuilder
from .registry import register

name = WorkflowName.GAME
@register(name)
def game_scenario():
    def turn_execution(faction : str):
        return PushWorkflow(
                name=WorkflowName.TURN,
                config=TurnConfig(faction)
            )
    
    return (
        ScenarioBuilder(name, config=GameConfig(factions=["moloch", "borgo"]))
        .tick()
        .then_execution(
            workflows=[turn_execution("moloch")]
        )

        .tick()
        .then_execution(
            workflows=[turn_execution("borgo")]
        )

        .tick()
        .then_execution(
            workflows=[GoToStep(index=0)],
            advance=False
        )
        
    ).build()