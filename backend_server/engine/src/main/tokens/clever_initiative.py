class CleverInitiative():
    initiative: list[int]
    is_used: list[bool]
    is_basic: list[bool]
    
    is_blocked_to_0: bool
    iniciative_boosts: int

    def __init__(self, initiative: list[int]) -> None:
        self.base_iniciative = list(initiative)
        self.initiative = list(initiative)
        self.is_used = [False for _ in self.initiative]
        self.is_basic = [True for _ in self.initiative]

        self.is_blocked_to_0 = False
        self.iniciative_boosts = 0

        self.num_of_new = 0

    def add_iniciative(self) -> None:
        if len(self.initiative) == 0:
            return

        initiatives = set(self.initiative)
        max_iniciative = max(initiatives)
        new_iniciative = None

        candidate = max_iniciative - 1
        while new_iniciative is None:
            if candidate not in initiatives:
                new_iniciative = candidate
                break
            candidate -= 1

        if new_iniciative is None:
            return

        data = list(zip(self.initiative, self.is_used, self.is_basic))
        data.append((new_iniciative, False, False))
        data.sort(key=lambda item: item[0], reverse=True)

        self.initiative = [initiative for initiative, _, _ in data]
        self.is_used = [is_used for _, is_used, _ in data]
        self.is_basic = [is_basic for _, _, is_basic in data]
            
    def remove_iniciative(self) -> None:     
        for i in range(len(self.initiative)-1, -1, -1):
            if self.is_basic[i] == False:
                self.initiative.pop(i)
                self.is_used.pop(i)
                self.is_basic.pop(i)
                return
            
    def begin_iniciative(self) -> None:
        self.initiative = list(self.base_iniciative)
        self.is_used = [False for _ in self.initiative]
        self.is_basic = [True for _ in self.initiative]
        self.is_blocked_to_0 = False
        self.iniciative_boosts = 0
        self.num_of_new = 0

    def end_booster_faze(self) -> None:
        for _ in range(self.num_of_new):
            self.add_iniciative()

    def activate(self, initiative: int) -> bool:
        if (initiative < 0): return True
        if (self.is_blocked_to_0):
            return initiative != 0
        
        for i in range(len(self.initiative)):
            if self.initiative[i] == initiative - self.iniciative_boosts and self.is_used[i] == False:
                self.is_used[i] = True
                return False
        return True
    
    def can_activate(self, initiative : int) -> bool:
        if (initiative < 0): return True
        if (self.is_blocked_to_0):
            return initiative != 0
    
        for i in range(len(self.initiative)):
            if self.initiative[i] == initiative - self.iniciative_boosts and self.is_used[i] == False:
                return False
        return True
            
    def export_iniciative(self) -> list[list[int | bool]]:
        return [
            [initiative, is_used, is_basic]
            for initiative, is_used, is_basic in zip(
                self.initiative,
                self.is_used,
                self.is_basic,
            )
        ]

    def import_iniciative(self, data: list[list[int | bool]]) -> None:
        self.initiative = [x[0] for x in data]
        self.is_used = [x[1] for x in data]
        self.is_basic = [x[2] for x in data]
        self.base_iniciative = [
            initiative
            for initiative, is_used, is_basic in data
            if is_basic
        ]

    def export_state(self) -> dict:
        return {
            "initiative": self.export_iniciative(),
            "is_blocked_to_0": self.is_blocked_to_0,
            "iniciative_boosts": self.iniciative_boosts,
            "num_of_new": self.num_of_new,
        }

    def import_state(self, data: dict | list[list[int | bool]]) -> None:
        if isinstance(data, list):
            self.import_iniciative(data)
            return

        self.import_iniciative(data.get("initiative", []))
        self.is_blocked_to_0 = data.get("is_blocked_to_0", False)
        self.iniciative_boosts = data.get("iniciative_boosts", 0)
        self.num_of_new = data.get("num_of_new", 0)
