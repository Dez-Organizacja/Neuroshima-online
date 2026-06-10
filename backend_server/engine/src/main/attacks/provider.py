from main.attacks.data import DirectedIntent, AttackConfig
from main.board.board import Hex
from main.tokens.board_token import BoardToken

class AttackProvider:
    @staticmethod
    def build_attack_intent(attack : AttackConfig, pos : Hex) -> DirectedIntent:
        return DirectedIntent(
            attaker_pos=pos,
            direction=attack.direction,
            attack_type=attack.attack_type,
            power=attack.power
        )

    @classmethod
    def get_attack_intents(cls, unit : BoardToken, pos : Hex) -> list[DirectedIntent]:
        return [
            cls.build_attack_intent(attack, pos)
            for attack in unit.get_attacks()
        ]