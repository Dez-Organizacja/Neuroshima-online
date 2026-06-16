from main.attacks.properties.data import AttackProperties
from main.attacks.config import AttackType

class AttackPropertiesFactory:
    _REGISTRY : dict[AttackType, AttackProperties] = {}

    @classmethod
    def register(cls, attack_type : AttackType):
        def decorator(properties : AttackProperties):
            cls._REGISTRY[attack_type] = properties
            return properties
        return decorator

    @classmethod
    def get(cls, attack_type : AttackType):
        return cls._REGISTRY[attack_type]()