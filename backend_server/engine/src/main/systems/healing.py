from main.board.board import Board, Hex
from main.rules.ability.heal import HealRules
from main.events.effects import HealEffect
from main.events.data import Effect
from typing import Protocol
from collections import defaultdict

class HasBoard(Protocol):
    board : Board

class HasFaction(Protocol):
    faction : Board

class HasHealingContext(Protocol):
    board : HasBoard
    faction : HasFaction

class HealingSystem:
    def __init__(self):
        self.rules = HealRules()
        self.my_healers : dict[Hex, list[Hex]] = defaultdict(list)
        self.my_targets : dict[Hex, list[Hex]] = defaultdict(list)

    def build_healing_options(self, board : Board, faction : str):
        self.my_healers.clear()
        self.my_targets.clear()

        for source in self.rules.get_sources(board, faction):
            for target in self.rules.non_healers_targets(board, source):
                self.my_healers[target].append(source)
                self.my_targets[source].append(target)

    @staticmethod
    def resolve(healer_pos : Hex, target_pos : Hex) -> HealEffect:
        return HealEffect(source_pos=healer_pos, target_pos=target_pos)

    def auto_heal(self) -> list[Effect]:
        result = []
        for source, targets in self.my_targets.items():
            if len(targets) > 1:
                continue
            target = targets[0]
            if len(self.my_healers[target]) > 1:
                continue
            result.append(self.resolve(source, target))

    def resolve_automatic(self, ctx : HasHealingContext) -> list[Effect]:
        self.build_healing_options(ctx.board, ctx.faction)
        return self.auto_heal()