from ..builder import ScenarioBuilder
from ..registry import ScenarioRegistry
from ..data import Scenario
from main.input.data import BoardAction, HandAction
from main.state.game_state import GameState
from main.state.contex import ActionContext

@ScenarioRegistry.register("place_action")
def place_action_scenario() -> Scenario:
    return (
        ScenarioBuilder(factions=["moloch", "borgo"])
        .when(HandAction(slot=0))
        .given(
            
        )
    )
