from random import shuffle
from main.tokens.registry import TokenConfigRegistry
from main.tokens.data import TokenKey
from main.tokens.pile import Pile

class PileFactory:
    @staticmethod
    def create_pile(faction : str) -> Pile:
        pile = Pile()

        for name in TokenConfigRegistry.get_faction_units(faction):
            config = TokenConfigRegistry.get(faction, name)
            for _ in range(config.unit_count):
                pile.add(name)

        shuffle(pile.tokens)
        return pile