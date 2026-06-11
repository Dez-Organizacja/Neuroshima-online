from .data import (
    Delta,
    TileRemove,
    TilePlace,
    TileRotate,
    TileDamage,
    HandAdd,
    HandRemove,
    StackPush,
    StackPop,
    StackSetIndex,
)
from main.workflows.data import WorkflowName, WorkflowInstance, WorkflowConfig
from main.input.data import ActionType, Button
from typing import Callable
from main.actions.available.data import AvailableStructure
from main.events.data import Event, OnClickData

# ----------- State Delta -----------
def tile_place(pos : tuple[int, int], name : str, faction : str, rotation : int = 0):
    def apply(delta : Delta):
        delta.board_delta.append(TilePlace(pos, name, faction, rotation))
    return apply


def tiles_remove(positions : list[tuple[int, int]]):
    def apply(delta: Delta):
        for pos in positions:
            delta.board_delta.append(TileRemove(pos=pos))
    return apply

def tile_rotate(pos: tuple[int, int], rotation: int):
    def apply(delta: Delta):
        delta.board_delta.append(TileRotate(pos=pos, rotation=rotation))
    return apply

def tile_damage(pos : tuple[int, int], damage : int = 1):
    def apply(delta : Delta):
        delta.board_delta.append(TileDamage(pos, damage))
    return apply

def hand_add(faction: str, cards: list[str]):
    def apply(delta: Delta):
        for card in cards:
            delta.hand_delta.append(HandAdd(faction=faction, card=card))
    return apply

def hand_remove(faction: str, index: int):
    def apply(delta: Delta):
        delta.hand_delta.append(HandRemove(faction=faction, index=index))
    return apply

def wf_data_delta(**data):
    def apply(delta: Delta):
        delta.wf_data_delta = data
    return apply

def stack_add(
    name: WorkflowName,
    config: WorkflowConfig | None = None,
    index : int | None = None,
):
    def apply(delta: Delta):
        workflow_config = config or WorkflowConfig()

        delta.stack_delta.append(
            StackPush(
                instance=WorkflowInstance(
                    name=name,
                    config=workflow_config,
                )
            )
        )
        if index is not None:
            delta.stack_delta.append(StackSetIndex(index=index))

    return apply

def stack_index_change(index: int):
    def apply(delta: Delta):
        delta.stack_delta.append(StackSetIndex(index=index))

    return apply

def stack_pop(count : int = 1):
    def apply(delta: Delta):
        for i in range(count):
            delta.stack_delta.append(StackPop())

    return apply

def stack_add_game_wf(factions : list[str]):
    return stack_add(
        name=WorkflowName.GAME,
        index=5, # znaznik ustawinoy na ture drugiej frakcji (tury frakcji indexy 4-5)
        config=WorkflowConfig(factions=factions),
    )

def stack_add_turn_wf(faction : str):
    return stack_add(
        name=WorkflowName.TURN,
        index=2,
        config=WorkflowConfig(faction=faction),
    )


def faction_delta(faction: str, turn : bool = False):
    def apply(delta: Delta):
        if turn:
            delta.turn_faction_delta = faction
        delta.faction_delta = faction

    return apply

def expected_step_index(index: int):
    def apply(delta: Delta):
        delta.expected_step_index = index

    return apply

def composed_function(*funcs : Callable[[Delta], None]):
    def apply(delta : Delta):
        for func in funcs:
            func(delta)
    return apply

def pushing_hand_wf_changes(slot : int):
    return composed_function(
        wf_data_delta(slot=slot, type=ActionType.HAND),
        stack_index_change(index=4),
        stack_add(
            name=WorkflowName.HAND, 
            index=1, 
        ),
    )

def action_workflow_config(slot) -> WorkflowConfig:
    return WorkflowConfig(on_click=OnClickData(discard_slot=slot))

def setup_turn(factions : list[str]):
    return composed_function(
        stack_add_game_wf(factions),
        stack_add_turn_wf(factions[0]),
        faction_delta(faction=factions[0], turn=True),
    )

def wf_data_clear():
    return composed_function(
        wf_data_delta(
            slot=None,
            unit_pos=None,
            target_pos=None,
            destination=None,
            rotation=None,
            type=None,
            button=None,
            decision=None,
        )
    )

def faction_tiles_place(
        faction : str,
        positions : list[tuple[int, int]],
        names : list[str],
        rotations : list[int],
):
    if len(positions) != len(names) or len(names) != len(rotations):
        raise ValueError("Faction tile placment wrong arrays sizes")
    
    return composed_function(
        *[tile_place(pos, name, faction, rotation)
        for pos, name,rotation in zip(positions, names, rotations)]
    )
            

# ----------- Available Actions -----------
def board(*positions : tuple[int, int]):
    def apply(actions : AvailableStructure):
        actions.board = list(positions)

    return apply

def tokens(*tokens : int):
    def apply(actions : AvailableStructure):
        for i in tokens:
            actions.hand[i] = True

    return apply

def buttons(*buttons : Button):
    def apply(actions : AvailableStructure):
        actions.buttons = list(buttons)
    return apply

