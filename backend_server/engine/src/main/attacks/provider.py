from main.attacks.data import DirectedIntent, AttackConfig, AttackType
from main.attacks.properties.factory import AttackPropertiesFactory
from main.board.board import Hex
from main.tokens.board_token import BoardToken

class AttackProvider:
    @staticmethod
    def boost_power(power : int, attack_type : AttackType, unit : BoardToken):
        return power + unit.get_attack_boost(attack_type)

    @classmethod
    def build_attack_intent(
        cls, 
        attack : AttackConfig, 
        pos : Hex, 
        unit : BoardToken
    ) -> DirectedIntent:
        return DirectedIntent(
            attaker_pos=pos,
            direction=attack.direction,
            properties=AttackPropertiesFactory.get(attack.attack_type),
            power=cls.boost_power(attack.power, attack.attack_type, unit),
        )

    @classmethod
    def get_attack_intents(cls, unit : BoardToken, pos : Hex) -> list[DirectedIntent]:
        return [
            cls.build_attack_intent(attack, pos, unit)
            for attack in unit.get_attacks()
        ]