from main.frakcje.base import Faction
from main.frakcje.builder import gauss, melee, shoot
from main.tokens.data import Ability, BattleAbility, Boost

unit = Faction("moloch")

units = [
    unit.HQ(boost=Boost.SHOOT).build(),

    unit.board("bloker", unit_count=2)
    .hp(3)
    .directions_of(armor=[0])
    .build(),

    unit.board("cyborg", unit_count=2)
    .hp(1)
    .attacks(shoot(directions=[0]))
    .initiatives([3])
    .build(),

    unit.board("dzialkogaussa", unit_count=1)
    .hp(2)
    .attacks(gauss(directions=[4]))
    .initiatives([1])
    .build(),

    unit.board("juggernaut", unit_count=1)
    .hp(2)
    .attacks(
        shoot(directions=[1]),
        melee(directions=[0], power=2),
    )
    .directions_of(armor=[0, 2, 4])
    .initiatives([1])
    .build(),

    unit.board("klaun", unit_count=1)
    .hp(2)
    .attacks(melee(directions=[0, 5]))
    .initiatives([2])
    .battle_ability(BattleAbility.EXPLOSIN)
    .build(),

    unit.board("lowca", unit_count=2)
    .hp(1)
    .attacks(melee(directions=[0, 1, 3, 5]))
    .initiatives([3])
    .build(),

    unit.board("obronca", unit_count=1)
    .hp(2)
    .attacks(shoot(directions=[0, 1, 5]))
    .initiatives([1])
    .build(),

    unit.board("opancerzonylowca", unit_count=2)
    .hp(2)
    .attacks(melee(directions=[0, 1, 2, 3, 4, 5]))
    .directions_of(armor=[0, 5])
    .initiatives([2])
    .build(),

    unit.board("opancerzonywartownik", unit_count=1)
    .hp(1)
    .attacks(shoot(directions=[0, 5]))
    .initiatives([2])
    .build(),

    unit.board("rozpruwacz", unit_count=1)
    .hp(1)
    .attacks(melee(directions=[0], power=2))
    .initiatives([2])
    .build(),

    unit.board("sieciarz", unit_count=1)
    .hp(1)
    .directions_of(wire=[0, 5])
    .build(),

    unit.board("szturmowiec", unit_count=1)
    .hp(2)
    .attacks(shoot(directions=[0]))
    .initiatives([1, 2])
    .build(),

    unit.board("wartownik", unit_count=1)
    .hp(1)
    .attacks(shoot(directions=[1, 5]))
    .directions_of(armor=[0])
    .initiatives([2])
    .build(),

    unit.board("oficer", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.SHOOT], directions=[1, 3, 5])
    .build(),

    unit.board("zwiadowca", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.INITIATIVE], directions=[0, 2, 4])
    .build(),

    unit.board("matka", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.NEW_INITIATIVE], directions=[0])
    .build(),

    unit.board("medyk", unit_count=2)
    .hp(1)
    .boosts(types=[Boost.HEAL], directions=[0, 2, 4])
    .build(),

    unit.board("mozg", unit_count=1)
    .hp(1)
    .boosts(types=[Boost.SHOOT, Boost.MELEE], directions=[0, 2, 4])
    .build(),

    unit.instant("bitwa", unit_count=4)
    .ability(Ability.BATTLE)
    .build(),

    unit.instant("ruch", unit_count=1)
    .ability(Ability.MOVE)
    .build(),

    unit.instant("odepchniecie", unit_count=5)
    .ability(Ability.PUSH)
    .build(),

    unit.instant("bomba", unit_count=1)
    .ability(Ability.BOMB)
    .build(),
]
