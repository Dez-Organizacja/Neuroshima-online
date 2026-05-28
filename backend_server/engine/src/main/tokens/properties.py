from enum import Enum
import main.frakcje.wszystkie_frakcje as allfractions

class Properties:
    def __init__(self, name: str, faction: str):
        self.data = allfractions.frakcje.get(
            faction, {}
        ).get(name, {})

        self.import_from_dict(self.data)

    def import_from_dict(self, data) -> None:
        self.__dict__.clear()

        for key, value in data.items():
            if isinstance(key, Enum):
                attr_name = key.name
            else:
                attr_name = str(key)

            if attr_name.isidentifier():
                setattr(self, attr_name, value)

    def to_dict(self) -> dict:
        # tu mozna zrobic by zwracal tylko te wazne
        return self.__dict__.copy()