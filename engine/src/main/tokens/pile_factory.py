from random import shuffle
import main.frakcje.wszystkie_frakcje as allfractions
from main.tokens.data import TokenKey
from main.tokens.pile import Pile

class PileFactory:
    @staticmethod
    def create_pile(fraction : str) -> Pile:
        pile = Pile()

        config = allfractions.frakcje.get(fraction, {})
        for name, data in config.items():

            for _ in range(data[TokenKey.UNIT_COUNT]):
                pile.add(name)

        shuffle(pile.tokens)
        return pile