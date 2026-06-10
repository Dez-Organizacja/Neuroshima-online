from main.workflows.data import WorkflowName
from main.input.data import ButtonAction, Button, ActionType
from main.events.flow import StartBattleEvent
from main.events.workflow import PushWorkflow, PopWorkflow

from .builder import ScenarioBuilder
from .registry import register

name = WorkflowName.START_BATTLE
@register(name)
def start_battle_scenario():
    return (
        ScenarioBuilder(name)
        .when(ButtonAction(name = Button.USE))
        .then_data_delta(button=Button.USE, type=ActionType.BUTTON)

        .tick()
        .then_execution(
            events=[StartBattleEvent()]
        )
    ).build()