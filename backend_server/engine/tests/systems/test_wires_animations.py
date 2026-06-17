from main.engine.resolver import Resolver
from main.events.effects import RecomputePassivesEffect
from main.rules.faction_manager import FactionManager
from main.state.context import ActionContext
from main.state.game_state import GameState


def test_resolver_adds_wire_animations_after_passive_recompute():
    state = GameState(
        factions=["testowa", "moloch"],
        turn_faction="testowa",
        active_faction="testowa",
    )
    state.board.put_token((2, 4), "sieciarz", "testowa")
    state.board.get_token((2, 4)).set_rotation(1)
    state.board.put_token((2, 6), "sztab", "moloch")

    ctx = ActionContext(
        state=state,
        faction_manager=FactionManager(state.factions),
    )

    Resolver().execute(ctx, [RecomputePassivesEffect()])

    wire_animations = [
        animation
        for animation in ctx.animations
        if animation.type == "set_wire"
    ]

    assert ctx.board.get_token((2, 6)).wired is True
    assert len(wire_animations) == 1
    assert wire_animations[0].pos == (2, 6)
    assert wire_animations[0].wired is True
