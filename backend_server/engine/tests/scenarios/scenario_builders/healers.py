from ..builder import ScenarioBuilder
from ..build_helpers import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.workflows.data import WorkflowName
from main.input.data import HandAction, BoardAction, Button, ButtonAction

@ScenarioRegistry.register("healer2")
def test_two_connected_healers() -> Scenario:
    factions = ["moloch", "posterunek"]
    return (
        ScenarioBuilder(factions)
        .given(
            push_game_wf(factions),
            setup_turn_wf(factions[0]),
            push_workflow(
                name(WorkflowName.DAMAGE_RESOLVE), 
                index(3), 
                config(factions=factions)
            ),
            push_workflow(name(WorkflowName.HEAL), config(faction="moloch")),
            board(
                faction_place(
                    "moloch",
                    tile((2, 0), "medyk", rotation=1),
                    tile((2, 2), "medyk", rotation=1),
                    tile((2, 4), "sztab"),
                ),
                unit((2, 4), wounds(2)),
            )
        )

        # CAPTURING WOUND FROM (2, 4)
        .when(BoardAction(pos=(2, 2)))
        .then(workflow(index(5)))
        .available_actions(
            positions((2, 4)),
            buttons(Button.CANCEL)
        )

        .when(BoardAction(pos=(2, 4)))
        .then(
            board(
                unit((2, 4), remove_wounds()),
                unit((2, 2), wounds(2))
            ),
            workflow(index(2))
        )
        .available_actions(
            buttons(Button.CANCEL, Button.YES, Button.NO)
        )
    ).build()