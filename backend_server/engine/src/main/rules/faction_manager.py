from main.tokens.data import TokenRelation

class FactionManager:
    def __init__(self, factions : list[str]):
        self.factions = factions

    @staticmethod
    def get_relation(faction1 : str, faction2 : str) -> TokenRelation | None:
        if faction1 is None or faction2 is None:
            return None
        return (
            TokenRelation.OWN 
            if faction1 == faction2 
            else TokenRelation.ENEMY
        )


    def get_enemy(self, my_faction):
        print(f"getting enemy of {my_faction}")
        for faction in self.factions:
            if(faction != my_faction):
                print(f"found enemy {faction}")
                return faction
            
    def get_faction(self, my_faction : str, relation : TokenRelation):
        for faction in self.factions:
            if self.get_relation(my_faction, faction) == relation:
                return faction
        raise ValueError(f"Not found faction of {relation} to {my_faction}")
    
    @staticmethod
    def are_enemies(faction1, faction2) -> bool:
        relation = FactionManager.get_relation(faction1, faction2)
        return relation == TokenRelation.ENEMY
    
    @staticmethod
    def are_allies(faction1, faction2) -> bool:
        relation = FactionManager.get_relation(faction1, faction2)
        return relation == TokenRelation.OWN