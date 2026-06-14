from importlib import import_module
from main.tokens.registry import TokenConfigRegistry
_BOOTSTRAPED = False

def register_factions():
    FACTIONS = [
        "moloch",
        "borgo",
        "testowa",
        "posterunek",
        "hegemonia",
    ]

    path = "main.frakcje"

    for faction in FACTIONS:
        lib = import_module(f"{path}.{faction}")
        for config in lib.units:
            TokenConfigRegistry.registry(config)

def register_targeting():
    import main.attacks.targeting.strategies

def register_attack_properties():
    import main.attacks.properties.properties

def bootstrap():
    global _BOOTSTRAPED

    if _BOOTSTRAPED:
        return
    
    _BOOTSTRAPED = True

    register_targeting()
    register_factions()
    register_attack_properties()