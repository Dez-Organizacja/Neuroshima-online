from main.frakcje.base import Faction
from main.frakcje.builder import melee, shoot
from main.tokens.data import Ability, Boost, TokenRelation

unit = Faction("posterunek")

units = [
    unit.HQ(boost=Boost.NEW_INITIATIVE).build(),
    
    unit.board("biegacz", unit_count=2)
    .hp(1)
    .attacks(melee(directions=[5]))
    .initiatives([2])
    .ability(Ability.MOVE)
    .build(),

    unit.board("ckm", unit_count=1)
    .hp(1)
    .attacks(shoot(directions=[0]))
    .initiatives([2, 1])
    .build(),

    unit.board("komandos", unit_count=5)
    .hp(1)
    .attacks(shoot(directions=[2]))
    .initiatives([3])
    .build(),

    unit.board("likwidator", unit_count=2)
    .hp(1)
    .attacks(shoot(directions=[4], power=2))
    .initiatives([2])
    .build(),

    unit.board("pancerzwspomagany", unit_count=1)
    .hp(1)
    .attacks(
        melee(directions=[0], power=2),
        shoot(directions=[5]),
    )
    .initiatives([3, 2])
    .ability(Ability.MOVE)
    .build(),

    unit.board("silacz", unit_count=1)
    .hp(1)
    .attacks(melee(directions=[0], power=2))
    .initiatives([3])
    .build(),

    unit.board("centrumrozpoznania", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.MOVE_RANGE])
    .build(),

    unit.board("dywersant", unit_count=1)
    .hp(1)
    .boosts(
        types=[Boost.MINUS_INITIATIVE],
        directions=[0, 1, 2, 3, 4, 5],
        target=TokenRelation.ENEMY,
    )
    .build(),

    unit.board("medyk", unit_count=2)
    .hp(1)
    .boosts(types=[Boost.HEAL], directions=[0, 1, 5])
    .build(),

    unit.board("oficer", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.SHOOT], directions=[0, 1, 2, 3, 4,    5])
    .build(),

    unit.board("skoper", unit_count=1)
    .hp(1)
    .boosts(
        types=[Boost.STEAL_BOOST],
        directions=[0, 1, 2, 3, 4, 5],
        target=TokenRelation.ENEMY,
    )
    .build(),

    unit.board("zwiadowca", unit_count=2)
    .hp(1)
    .boosts(types=[Boost.INITIATIVE], directions=[0, 2, 4])
    .build(),

    unit.instant("bitwa", unit_count=6)
    .ability(Ability.BATTLE)
    .build(),

    unit.instant("ruch", unit_count=7)
    .ability(Ability.MOVE)
    .build(),

    unit.instant("snajper", unit_count=1)
    .ability(Ability.SNIPER)
    .build(),
]
