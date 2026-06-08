from .data import (
    Delta,
    TileDelta,
    TileRemove,
    TilePlace,
    HandAdd,
    HandRemove,
    StackPush,
    StackPop,
    StackSetIndex,
)
from main.workflows.data import WorkflowName, WorkflowInstance, WorkflowConfig

def tile_delta(pos : tuple[int, int], **data):
    def apply(delta : Delta):
        delta.board_delta.append(TileDelta(pos=pos, unit=data))
    return apply
    
def tile_place(pos : tuple[int, int], name : str, faction : str):
    def apply(delta : Delta):
        delta.board_delta.append(TilePlace(pos, name, faction))
    return apply

def tile_remove(pos: tuple[int, int]):
    def apply(delta: Delta):
        delta.board_delta.append(TileRemove(pos=pos))
    return apply

def hand_add(faction: str, card: str):
    def apply(delta: Delta):
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

def stack_pop():
    def apply(delta: Delta):
        delta.stack_delta.append(StackPop())

    return apply

def stack_add_game_wf(factions : list[str]):
    return stack_add(
        name=WorkflowName.GAME,
        index=1,
        config=WorkflowConfig(factions=factions),
    )

def stack_add_turn_wf(faction : str):
    return stack_add(
        name=WorkflowName.TURN,
        index=2,
        config=WorkflowConfig(faction=faction),
    )


def faction_delta(faction: str):
    def apply(delta: Delta):
        delta.faction_delta = faction

    return apply

def expected_step_index(index: int):
    def apply(delta: Delta):
        delta.expected_step_index = index

    return apply