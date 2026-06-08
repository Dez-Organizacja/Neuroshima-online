from main.tokens.data import TokenType, Boost
from main.frakcje.builder import token, melee

class Faction:
    def __init__(self, name : str):
        self.name = name

    def board(self, name : str, unit_count : int):
        return token(name, self.name, unit_count, type=TokenType.BOARD)

    def instant(self, name : str, unit_count : int):
        return token(name, self.name, unit_count, type=TokenType.INSTANT)
    
    def HQ(
            self, 
            hp : int = 20, 
            boost : Boost | None = None, 
            initiatives : list[int] = [0],
        ):
        sztab = (
            self.board("sztab", unit_count=1)
            .hp(hp)
            .attacks(melee(directions=[i for i in range(0)]))
            .initiatives(initiatives)
        )
        if boost is not None:
            sztab.boosts(types=[boost], directions=[i for i in range(0)])

        return sztab 