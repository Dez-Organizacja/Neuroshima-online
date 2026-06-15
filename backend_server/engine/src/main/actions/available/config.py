from dataclasses import dataclass
from main.input.data import Button
from typing import Callable
from main.state.context import ActionContext

ButtonsGetter = Callable[[ActionContext], list[Button]]
PositionsGetter = Callable[[ActionContext], list[tuple[int, int]]]
TokensGetter = Callable[[ActionContext], dict[str, list[int]]]

def no_buttons(ctx : ActionContext) -> list[Button]:
    return []

def no_positions(ctx : ActionContext) -> list[tuple[int, int]]:
    return []

def no_tokens(ctx : ActionContext) -> list[int]:
    return []

@dataclass
class AvailableActionProvider:
    get_buttons : ButtonsGetter = no_buttons
    get_positions : PositionsGetter = no_positions
    get_tokens : TokensGetter = no_tokens