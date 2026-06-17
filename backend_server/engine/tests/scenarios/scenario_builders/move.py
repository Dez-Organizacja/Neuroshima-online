from ..builder import ScenarioBuilder
from ..build_helpers import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.input.data import BoardAction, RotationAction

@ScenarioRegistry.register("move1")
def test_centrum_rozpoznania_gives_move_of_range_2():
    factions = ["posterunek", "moloch"]
    return (
        ScenarioBuilder(factions)
        .given(
            setup_action(factions),
            board(
                faction_place(
                    "posterunek",
                    tile((2, 4), "sztab"),
                    tile((2, 2), "centrumrozpoznania"),
                    tile((4, 2), "biegacz")
                ),
                place((0, 2), "sztab", "moloch")
            )
        )

        .when(BoardAction(pos=(4, 2)))
        .then(
            workflow(name(WorkflowName.MOVE), index(1))
        )
        .available_actions(
            positions((3, 1), (3, 3), (4, 4), (4, 2)),
        )

        .when(BoardAction(pos=(4, 4)))
        .then(
            workflow(name(WorkflowName.ROTATE), index(0)),
            used_move("posterunek"),
            board(move((4, 2), (4, 4))),
        )
        .available_actions(
            positions((4, 4)),
            buttons()
        )


        .when(RotationAction(1))
        .then(
            workflow(name(WorkflowName.MOVE), index(1)),
            board(unit((4, 4), rotate(1)))
        )

        .available_actions(
            positions((3, 3), (3, 5), (4, 2), (4, 6), (4, 4))
        )

        .when(BoardAction(pos=(4, 2)))
         .then(
            workflow(name(WorkflowName.ROTATE), index(0)),
            used_move("posterunek"),
            board(move((4, 4), (4, 2))),
        )
        .available_actions(
            positions((4, 2)),
            buttons()
        )
    ).build()