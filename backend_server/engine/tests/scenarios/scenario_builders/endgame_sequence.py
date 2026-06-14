from ..builder import ScenarioBuilder
from ..build_helpers import *
from ..data import Scenario
from ..registry import ScenarioRegistry
from main.input.data import BoardAction, Button, ButtonAction

@ScenarioRegistry.register("endgame1")
def endgame_scenario() -> Scenario:
    factions = ["moloch", "borgo"]
    return (
        ScenarioBuilder(factions)
        .given(
            phase(Phase.ENDGAME),
            push_workflow(
                name(WorkflowName.ENDGAMESEQUENCE),
                index(0),
                config(factions=factions),
            ),
            # hand("borgo", draw(["zabojca", "sieciarz"])),
            board(
                faction_place(
                    "moloch",
                    tile((2, 4), "sztab"),
                    tile((2, 0), "cyborg"),
                ),
                faction_place(
                    "borgo",
                    tile((0, 2), "sztab"),
                    tile((1, 3), "mutek", rotation=1),
                )
            )
        )

        .when(ButtonAction(Button.END_TURN)) #end borgo's turn
        .then(
            board(
                unit((0, 2), damage()),
                unit((2, 4), damage()),
                tiles_remove([(1, 3)]), # Last Battle
                # Draw
            ),
            set_faction("moloch", turn=True), # goes to moloch's turn
            workflow(*turn_workflow("moloch"))
        )

        .when(ButtonAction(Button.END_TURN)) # end moloch's turn
        .then(
            set_faction("borgo"),
            workflow(*turn_workflow("borgo")), # goes to borgo's turn
        )

        .when(ButtonAction(Button.END_TURN)) #end borgo's turn
        .then(
            board(unit((0, 2), damage())), #Battle
            phase(Phase.GAMEOVER),
            set_faction("", turn=True),
            workflow(name(WorkflowName.GAMEOVER), index(0))
        )
        .available_actions(
            positions(),
            buttons(),
            tokens(),
        )
    ).build()

@ScenarioRegistry.register("endgame2")
def endgame_finish_after_first_battle_scenario() -> Scenario:
    factions = ["moloch", "borgo"]
    return (
        ScenarioBuilder(factions)
        .given(
            phase(Phase.ENDGAME),
            push_workflow(
                name(WorkflowName.ENDGAMESEQUENCE),
                index(0),
                config(factions=factions),
            ),
            board(
                faction_place(
                    "moloch",
                    tile((2, 4), "sztab"),
                    tile((2, 0), "cyborg"),
                ),
                faction_place(
                    "borgo",
                    tile((0, 2), "sztab"),
                )
            )
        )

        .when(ButtonAction(Button.END_TURN)) #end borgo's turn
        .then(
            board(
                unit((0, 2), damage()), # Last Battle
            ),
            phase(Phase.GAMEOVER),
            set_faction("", turn=True),
            workflow(name(WorkflowName.GAMEOVER), index(0))
        )
        .available_actions(
            positions(),
            buttons(),
            tokens(),
        )
    ).build()