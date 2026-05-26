from dataclasses import dataclass, field

@dataclass
class Pile:
    tokens : list[str] = field(default_factory=list)
    
    def add(self, name : str):
        self.tokens.append(name)

    def remove(self, name : str) -> str:
        self.tokens.remove(name)

    def draw(self) -> str:
        return self.tokens.pop()
    
    @property
    def empty(self):
        return len(self.tokens) == 0

    @classmethod
    def from_list(self, data):
        return Pile(data)

    def to_list(self) -> list[str]:
        return self.tokens