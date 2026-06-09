from main.frakcje.base import Faction
from main.tokens.data import Ability

unit = Faction("testowa")

units = [
    unit.board("sieciarz", unit_count=10)
    .hp(1)
    .directions_of(wire=[0])
    .build(),

    unit.board("dwu-sieciarz", unit_count=10)
    .hp(1)
    .directions_of(wire=[0, 1])
    .build(),

    unit.instant("snajper", unit_count=1)
    .ability(Ability.SNIPER)
    .build(),
]
