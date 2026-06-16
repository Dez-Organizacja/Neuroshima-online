from main.state.game_state import GameState
from main.attacks.data import DirectedIntent, TargetedIntent
from main.attacks.properties.data import AttackProperties
from main.attacks.targeting.data import TargetingType

def test():
    properties = AttackProperties(targeting_type=TargetingType.ADJACENT)
    state = GameState(factions=["moloch", "borgo"])
    state.pending_attacks.extend([
        DirectedIntent(attacker_pos=(1, 1), direction=1, properties=properties),
        TargetedIntent(target_pos=(1, 3)),
    ])

    data = state.to_dict()
    resotored_state = GameState.from_dict(data)
    assert state.pending_attacks == resotored_state.pending_attacks
