from main.frakcje.base import Faction
from main.frakcje.builder import melee, shoot
from main.tokens.data import Ability, Boost

unit = Faction("hegemonia")

units = [
    unit.HQ(boost=Boost.MELEE).build(),

    # unit.board("biegacz", unit_count=3)
    # .hp(1)
    # .attacks(melee(directions=[0]))
    # .initiatives([2])
    # .ability(Ability.MOVE)
    # .build(),

    # unit.board("bydlak", unit_count=1)
    # .hp(1)
    # .attacks(
    #     melee(directions=[0], power=2),
    #     melee(directions=[1, 5]),
    # )
    # .initiatives([2])
    # .build(),

    unit.board("ganger", unit_count=4)
    .hp(1)
    .attacks(melee(directions=[5]))
    .initiatives([3])
    .build(),

    # unit.board("gladiator", unit_count=1)
    # .hp(2)
    # .attacks(melee(directions=[0, 1, 5], power=2))
    # .directions_of(armor=[0, 1, 5])
    # .initiatives([1])
    # .build(),

    unit.board("sieciarz", unit_count=2)
    .hp(1)
    .directions_of(wire=[1])
    .build(),

    # unit.board("straznik", unit_count=1)
    # .hp(2)
    # .attacks(melee(directions=[0, 4, 5]))
    # .initiatives([2])
    # .build(),

    unit.board("supersieciarz", unit_count=1)
    .hp(1)
    .attacks(melee(directions=[3]))
    .directions_of(wire=[2, 4])
    .initiatives([2])
    .build(),

    unit.board("uniwersalnyzolnierz", unit_count=3)
    .hp(1)
    .attacks(
        melee(directions=[5]),
        shoot(directions=[5]),
    )
    .initiatives([3])
    .build(),

    # unit.board("boss", unit_count=1)
    # .hp(1)
    # .boosts(types=[Boost.MELEE], directions=[0, 5])
    # .boosts(types=[Boost.INITIATIVE], directions=[0, 5])
    # .build(),

    # # unit.board("kwatermistrz", unit_count=1)
    # # .hp(1)
    # # .boosts(types=[Boost.MELEE_TO_SHOOT], directions=[0]) xdxdxdxd
    # # .build(),
    
    unit.board("kwatermistrz", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.MELEE], directions=[0, 1, 5])
    .boosts(types=[Boost.SHOOT], directions=[0, 1, 5])
    .build(),

    # unit.board("oficer1", unit_count=2)
    # .hp(1)
    # .boosts(types=[Boost.MELEE], directions=[0, 5])
    # .build(),

    # unit.board("oficer2", unit_count=1)
    # .hp(1)
    # .boosts(types=[Boost.MELEE], directions=[0, 1, 5])
    # .build(),

    # unit.board("transport", unit_count=1)
    # .hp(1)
    # .boosts(types=[Boost.MOVE_ABILITY], directions=[0, 1, 2, 3, 4, 5])
    # .build(),

    # unit.board("zwiadowca", unit_count=1)
    # .hp(1)
    # .boosts(types=[Boost.INITIATIVE], directions=[0, 1, 5])
    # .build(),

    unit.instant("bitwa", unit_count=5)
    .ability(Ability.BATTLE)
    .build(),

    # unit.instant("ruch", unit_count=3)
    # .ability(Ability.MOVE)
    # .build(),

    # unit.instant("odepchniecie", unit_count=2)
    # .ability(Ability.PUSH)
    # .build(),

    unit.instant("snajper", unit_count=1)
    .ability(Ability.SNIPER)
    .build(),
]
