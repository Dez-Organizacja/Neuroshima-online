from dataclasses import dataclass
from main.utils.variable import Bottom
from typing import Callable
from main.state.contex import ActionContext

BottomsGetter = Callable[[ActionContext], list[Bottom]]
PositionsGetter = Callable[[ActionContext], list[tuple[int, int]]]
TokensGetter = Callable[[ActionContext], dict[str, list[int]]]

def no_bottoms(ctx : ActionContext) -> list[Bottom]:
    return []

def no_positions(ctx : ActionContext) -> list[tuple[int, int]]:
    return []

def no_tokens(ctx : ActionContext) -> dict[str, list[int]]:
    return {}

@dataclass
class AvActionsConfig:
    get_bottoms : BottomsGetter = no_bottoms
    get_positions : PositionsGetter = no_positions
    get_tokens : TokensGetter = no_tokens