from dataclasses import dataclass, field

class CleverInitiative():
    initiative: list[int]
    is_used: list[bool]
    is_basic: list[bool]
    
    is_blocked_to_0: bool
    initiative_boosts: int

    def __init__(self, initiative: list[int]) -> None:
        self.base_initiative = list(initiative)
        self.initiative = list(initiative)
        self.is_used = [False for _ in self.initiative]
        self.is_basic = [True for _ in self.initiative]

        self.is_blocked_to_0 = False
        self.initiative_boosts = 0

        self.num_of_new = 0
        self.num_of_old = 0

    def add_initiative(self) -> None:
        if len(self.initiative) == 0:
            return

        initiatives = set(self.initiative)
        max_initiative = max(initiatives)
        new_initiative = None

        candidate = max_initiative - 1
        while new_initiative is None:
            if candidate not in initiatives:
                new_initiative = candidate
                break
            candidate -= 1

        if new_initiative is None:
            return

        data = list(zip(self.initiative, self.is_used, self.is_basic))
        data.append((new_initiative, False, False))
        data.sort(key=lambda item: item[0], reverse=True)

        self.initiative = [initiative for initiative, _, _ in data]
        self.is_used = [is_used for _, is_used, _ in data]
        self.is_basic = [is_basic for _, _, is_basic in data]
            
    def remove_initiative(self) -> None:     
        for i in range(len(self.initiative)-1, -1, -1):
            if self.is_basic[i] == False:
                self.initiative.pop(i)
                self.is_used.pop(i)
                self.is_basic.pop(i)
                return
            
    def begin_initiative(self) -> None:
        self.initiative = list(self.base_initiative)
        self.is_blocked_to_0 = False
        self.initiative_boosts = 0
        self.num_of_new = 0

    def end_booster_faze(self) -> None:
        while (self.num_of_new > self.num_of_old):
            self.add_initiative()
            self.num_of_old += 1
        
        while (self.num_of_old > self.num_of_new):
             self.remove_initiative()
             self.num_of_old -= 1

    def mark_activated(self, initiative : int) -> None:
        self.activate(initiative)

    def activate(self, initiative: int) -> bool:
        if (initiative < 0 or len(self.initiative) == 0): 
            return False
        
        if (self.is_blocked_to_0):
            return initiative == 0
        
        if initiative == 0:
            for initiative, is_used in zip(self.initiative, self.is_used):
                if initiative <= 0 and is_used == False:
                    return True
            return False
        
        for i in range(len(self.initiative)):
            if self.initiative[i] == initiative - self.initiative_boosts and self.is_used[i] == False:
                self.is_used[i] = True
                return True
        return False
    
    def can_activate(self, initiative : int) -> bool:
        if (initiative < 0): return True
        if (self.is_blocked_to_0):
            return initiative != 0
    
        for i in range(len(self.initiative)):
            if self.initiative[i] == initiative - self.initiative_boosts and self.is_used[i] == False:
                return False
        return True
        

    def to_dict(self) -> dict:
        return {
            "initiative": self.initiative,
            "is_used": self.is_used,
            "is_basic": self.is_basic,
            "num_of_old": self.num_of_new,
        }

    def from_dict(self, data: dict) -> None:
        self.initiative = data.get("initiative", [])
        self.is_used = data.get("is_used", [False for _ in self.initiative])
        self.is_basic = data.get("is_basic", [True for _ in self.initiative])
        self.base_initiative = [
            initiative
            for initiative, is_used, is_basic in zip(self.initiative, self.is_used, self.is_basic)
            if is_basic
        ]
        self.is_blocked_to_0 = data.get("is_blocked_to_0", False)
        self.num_of_new = data.get("num_of_old", 0)
