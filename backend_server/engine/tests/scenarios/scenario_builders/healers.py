from ..builder import ScenarioBuilder
from ..build_helpers import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.workflows.data import WorkflowName
from main.input.data import HandAction, BoardAction, Button, ButtonAction

def healers_setup(factions : list[str], board_setup : list[Callable[[Board], None]]):
    return [
        push_game_wf(factions),
        setup_turn_wf(factions[0]),
        push_workflow(
            name(WorkflowName.DAMAGE_RESOLVE), 
            index(3), 
            config(factions=factions)
        ),
        push_workflow(name(WorkflowName.HEAL), config(faction=factions[0])),
        board(*board_setup)
    ]

@ScenarioRegistry.register("healer1")
def test_two_connected_healers() -> Scenario:
    factions = ["moloch", "posterunek"]
    board_setup = [
        faction_place(
            "moloch",
            tile((2, 0), "medyk", rotation=1),
            tile((2, 2), "medyk", rotation=1),
            tile((2, 4), "sztab"),
        ),
        unit((2, 4), wounds(2)),
    ]
    return (
        ScenarioBuilder(factions)
        .given(
            *healers_setup(factions, board_setup)
        )

        # CAPTURING WOUND FROM (2, 4)
        .when(BoardAction(pos=(2, 4)))
        .then(workflow(index(5)))
        .available_actions(
            positions((2, 2)),
            buttons(Button.CANCEL)
        )

        .when(BoardAction(pos=(2, 2)))
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

@ScenarioRegistry.register("healer2")
def steal_boosted_healer_connected_to_own_healer() -> Scenario:
    factions = ["posterunek", "moloch"]
    board_setup = [
        faction_place(
            "posterunek",
            tile((2, 2), "medyk"),
            tile((2, 4), "skoper"),
            tile((1, 5), "sztab"),
        ),
        unit((1, 5), wounds(1)),
        place((1, 3), "medyk", "moloch", rotation=1),
    ]
    return (
        ScenarioBuilder(factions)
        .given(*healers_setup(factions, board_setup))

        .when(BoardAction(pos=(1, 5)))
        .then(workflow(index(5)))
        .available_actions(
            positions((1, 3)),
            buttons(Button.CANCEL)
        )

        .when(BoardAction(pos=(1, 3)))
        .then(
            board(
                unit((1, 5), remove_wounds()),
                tiles_remove([(1, 3)])
            ),
            workflow(name(WorkflowName.ACTION), index(1))
        )
        .available_actions(
            buttons(Button.END_TURN)
        )
    )