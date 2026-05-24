from dataclasses import dataclass, field

@dataclass
class Hand():
    tokens : list[str] = field(default_factory=list)

    @property
    def size(self):
        return len(self.tokens)

    def remove(self, slot : int):
        self.tokens.pop(slot)

    def add(self, token : str):
        self.tokens.append(token)

    def get(self, place : int) -> str:
        if(place < 0 or place >= len(self.hand)):
            return None
        return self.tokens[place]

    @classmethod
    def form_list(self, data : list[str]):
        return Hand(data)

    def to_list(self) -> list[str]:
        return self.tokens
    