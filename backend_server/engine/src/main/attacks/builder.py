from main.attacks.data import AttackConfig, DirectedAttackIntent
from main.rules.attacks import get_targeting

def build_intent(
    attack : AttackConfig,
    attacker_pos : tuple[int, int],
) -> DirectedAttackIntent:
    return DirectedAttackIntent(
        attaker_pos=attacker_pos,
        direction=attack.direction,
        targeting=get_targeting(attack.attack_type),
        power=attack.power
    )