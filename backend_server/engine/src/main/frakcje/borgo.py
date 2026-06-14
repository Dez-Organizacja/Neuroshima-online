from main.frakcje.base import Faction
from main.frakcje.builder import melee, shoot
from main.tokens.data import Ability, Boost

unit = Faction("borgo")

units = [
    unit.HQ(boost=Boost.INITIATIVE).build(),

    # unit.board("mutek", unit_count=6)
    # .hp(1)
    # .attacks(melee(directions=[0, 1, 5]))
    # .initiatives([2])
    # .build(),

    unit.board("nozownik", unit_count=4)
    .hp(1)
    .attacks(melee(directions=[4, 5]))
    .initiatives([3])
    .build(),

    # unit.board("sieciarz", unit_count=2)
    # .hp(1)
    # .attacks(melee(directions=[2], power=3))
    # .directions_of(wire=[2])
    # .initiatives([1])
    # .build(),

    # unit.board("supermutant", unit_count=1)
    # .hp(2)
    # .attacks(
    #     melee(directions=[0], power=2),
    #     melee(directions=[1, 5]),
    # )
    # .directions_of(armor=[0, 1, 5])
    # .initiatives([2])
    # .build(),

    # unit.board("silacz", unit_count=2)
    # .hp(1)
    # .attacks(melee(directions=[0], power=2))
    # .initiatives([2])
    # .build(),

    # unit.board("zabojca", unit_count=2)
    # .hp(1)
    # .attacks(shoot(directions=[5]))
    # .initiatives([3])
    # .ability(Ability.MOVE)
    # .build(),

    unit.board("medyk", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.HEAL], directions=[0, 1, 5])
    .build(),

    # unit.board("oficer", unit_count=2)
    # .hp(1)
    # .boosts(types=[Boost.MELEE], directions=[0, 1, 5])
    # .build(),

    # unit.board("superoficer", unit_count=1)
    # .hp(2)
    # .boosts(types=[Boost.MELEE], directions=[0, 1, 5])
    # .build(),

    # unit.board("zwiadowca", unit_count=2)
    # .hp(1)
    # .boosts(types=[Boost.INITIATIVE], directions=[0, 1, 5])
    # .build(),

    # unit.instant("bitwa", unit_count=6)
    # .ability(Ability.BATTLE)
    # .build(),

    # unit.instant("ruch", unit_count=4)
    # .ability(Ability.MOVE)
    # .build(),

    # unit.instant("granat", unit_count=1)
    # .ability(Ability.GRENADE)
    # .build(),
]
