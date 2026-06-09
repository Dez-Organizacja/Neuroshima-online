from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from main.tokens.board_token import BoardToken
else:
    BoardToken = Any

class CleverInitiative:
    @staticmethod
    def add_initiative(token: BoardToken) -> None:
        modif = token.state.modifiers
        if not modif.initiatives:
            return

        initiatives = set(modif.initiatives)
        candidate = max(initiatives) - 1
        while candidate in initiatives:
            candidate -= 1

        data = list(zip(modif.initiatives, modif.is_used, modif.is_basic))
        data.append((candidate, False, False))
        data.sort(key=lambda item: item[0], reverse=True)

        modif.initiatives = [initiative for initiative, _, _ in data]
        modif.is_used = [is_used for _, is_used, _ in data]
        modif.is_basic = [is_basic for _, _, is_basic in data]

    @staticmethod
    def remove_initiative(token: BoardToken) -> None:
        modif = token.state.modifiers
        for index in range(len(modif.initiatives) - 1, -1, -1):
            if not modif.is_basic[index]:
                modif.initiatives.pop(index)
                modif.is_used.pop(index)
                modif.is_basic.pop(index)
                return

    @staticmethod
    def begin_initiative(token: BoardToken) -> None:
        modif = token.state.modifiers
        modif.initiatives = list(token.config.initiative)
        modif.is_used = [False for _ in modif.initiatives]
        modif.is_basic = [True for _ in modif.initiatives]
        modif.num_of_old = 0
        modif.is_blocked_to_0 = False
        modif.initiative_boosts = 0
        modif.num_of_new = 0

    @staticmethod
    def end_booster_faze(token: BoardToken) -> None:
        modif = token.state.modifiers

        while modif.num_of_new > modif.num_of_old:
            CleverInitiative.add_initiative(token)
            modif.num_of_old += 1

        while modif.num_of_old > modif.num_of_new:
            CleverInitiative.remove_initiative(token)
            modif.num_of_old -= 1

    @staticmethod
    def mark_activated(token: BoardToken, initiative: int) -> bool:
        return CleverInitiative.activate(token, initiative)

    @staticmethod
    def can_activate(token: BoardToken, initiative: int) -> bool:
        modif = token.state.modifiers

        if initiative < 0:
            return False

        if modif.is_blocked_to_0:
            if initiative != 0:
                return False
            return False

        if initiative == 0:
            return any(
                value <= 0 and not is_used
                for value, is_used in zip(modif.initiatives, modif.is_used)
            )

        target = initiative - modif.initiative_boosts
        return any(
            value == target and not is_used
            for value, is_used in zip(modif.initiatives, modif.is_used)
        )
    
    @staticmethod
    def activate(token: BoardToken, initiative: int) -> bool:
        if not CleverInitiative.can_activate(token, initiative):
            return False

        modif = token.state.modifiers
        target = initiative - modif.initiative_boosts
        for index in range(len(modif.initiatives)):
            if modif.initiatives[index] == target and not modif.is_used[index]:
                modif.is_used[index] = True
                return True

        return False

    @staticmethod
    def to_dict(token: BoardToken) -> dict:
        modif = token.state.modifiers
        return {
            "initiative": list(modif.initiatives),
            "is_used": list(modif.is_used),
            "is_basic": list(modif.is_basic),
            "num_of_old": modif.num_of_old,
            "is_blocked_to_0": modif.is_blocked_to_0,
            "initiative_boosts": modif.initiative_boosts,
            "num_of_new": modif.num_of_new,
        }

    @staticmethod
    def from_dict(token: BoardToken, data: dict) -> None:
        modif = token.state.modifiers
        modif.initiatives = list(data.get("initiative", []))
        modif.is_used = list(data.get("is_used", [False for _ in modif.initiatives]))
        modif.is_basic = list(data.get("is_basic", [True for _ in modif.initiatives]))
        modif.num_of_old = data.get("num_of_old", 0)
        modif.is_blocked_to_0 = data.get("is_blocked_to_0", False)
        modif.initiative_boosts = data.get("initiative_boosts", 0)
        modif.num_of_new = data.get("num_of_new", modif.num_of_old)
