from main.board.board import Board, Hex
from main.state.game_state import GameState
from main.tokens.board_token import BoardToken
from main.tokens.hand import Hand
from main.workflows.data import WorkflowName, WorkflowInstance
from main.input.data import Button
from typing import Callable
from main.actions.available.data import AvailableStructure
from main.utils.variable import Phase

# ----------- Helpers -----------
def _composed_function(*funcs : Callable[[GameState], None]):
    def apply(*args):
        for func in funcs:
            func(*args)
    return apply

def _set_attributes(obj, **data):
    for key, value in data.items():
        setattr(obj, key, value)

# ----------- Board changes -----------

def place(pos : tuple[int, int], name : str, faction : str, rotation : int = 0):
    def apply(board : Board):
        board.put_token(pos, name, faction)
        board.get_token(pos).set_rotation(rotation)
    return apply

def tile(pos : Hex, name : str, rotation : int = 0):
    def build(faction : str):
        return place(pos, name, faction, rotation)
    return build

def tiles_remove(positions : list[tuple[int, int]]):
    def apply(board : Board):
        for pos in positions:
            board.remove_token(pos)
    return apply

def rotate(rotation: int):
    def apply(unit : BoardToken):
        unit.set_rotation(rotation)
    return apply

def damage(damage : int = 1):
    def apply(unit : BoardToken):
        unit.add_damage(damage)
    return apply

def wounds(*wounds : int):
    def apply(unit : BoardToken):
        unit.wounds.extend(wounds)
    return apply    

def remove_wounds(index : int = 0):
    def apply(unit : BoardToken):
        unit.wounds.pop(index)
    return apply    
    
def unit(pos : Hex, *funcs : Callable[[BoardToken], None]):
    def apply(board : Board):
        for func in funcs:
            func(board.get_token(pos))
    return apply

def faction_place(faction : str, *funcs : Callable[[str], Callable[[Board], None]]):
    return _composed_function(
        *[
            func(faction)
            for func in funcs
        ]
    )

def board(*funcs : Callable[[Board], None]):
    def apply(state : GameState):
        for func in funcs:
            func(state.board)
    return apply

# ----------- Hand changes -----------
def hand(faction : str, *funcs : Callable[[Hand], None]):
    def apply(state : GameState):
        for func in funcs:
            func(state.players[faction].hand)
    return apply

def draw(cards: list[str]):
    def apply(hand : Hand):
        for card in cards:
            hand.add(card)
    return apply

def discard(index: int):
    def apply(hand : Hand):
        hand.remove(index)
    return apply

# ----------- Faction changes -----------
def set_faction(faction: str, turn = True):
    def apply(state : GameState):
        state.active_faction = faction
        if turn:
            state.turn_faction = faction
    return apply

# ----------- Top workflow changes -----------
def index(index : int):
    def apply(workflow : WorkflowInstance):
        workflow.current_step_index = index
    return apply

def config(**data):
    def apply(workflow : WorkflowInstance):
        _set_attributes(workflow.config, **data)
    return apply

def name(name : WorkflowName):
    def apply(workflow : WorkflowInstance):
        # print(f"name: {name}")
        workflow.name = name
    return apply

def workflow(*funcs : Callable[[WorkflowInstance], None]):
    def apply(state : GameState):
        for func in funcs:
            func(state.workflow_stack[-1])
    return apply

def turn_workflow(faction : str): #index = 2 to waiting step
    return [
        name(WorkflowName.TURN),
        index(2),
        config(faction=faction),
    ]

def phase(phase : Phase):
    def apply(state : GameState):
        state.phase = phase
    return apply

# ----------- setup -----------
def push_workflow(
        *funcs : Callable[[WorkflowInstance], None]
    ):
    def apply(state : GameState):
        # print("PUSH WORKFLOW APPLYING")
        # print(type(state))
        state.workflow_stack.append(WorkflowInstance(name=""))
        workflow(*funcs)(state)
    return apply

def push_game_wf(factions : list[str]) -> Callable[[GameState], None]:
    return push_workflow(
        name(WorkflowName.GAME), 
        index(5), #index na ture drugie frakcj
        config(factions=factions)
    )

def setup_turn_wf(faction : str) -> Callable[[GameState], None]:
    return _composed_function(
        push_workflow(*turn_workflow(faction)),
        set_faction(faction, turn=True),
    )

def wf_data_setup(**data):
    def apply(state : GameState):
        for key, value in data.items():
            if not hasattr(state.workflow_data, key):
                raise ValueError(f"Workflow data doesn't have argument {key}")
            setattr(state.workflow_data, key, value)
    return apply

def build_from_hand_action_wfs(
        factions : list[str], 
        wf_data_setup_func : Callable[[GameState], None] | None = None,
    ):
    wf_data_setup_func = wf_data_setup_func or wf_data_setup(slot=0)

    return _composed_function(
        wf_data_setup_func,
        push_game_wf(factions),
        setup_turn_wf(faction=factions[0]),
        push_workflow(name(WorkflowName.ACTION),index(3)),
        push_workflow(name(WorkflowName.HAND)),
    )

# ----------- Available Actions -----------
def positions(*positions : tuple[int, int]):
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