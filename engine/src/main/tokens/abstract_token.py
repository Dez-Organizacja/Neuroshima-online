from abc import ABC, abstractmethod

class Token(ABC):
    def __init__(self, name, fraction, token_type):
        self.name = name
        self.fraction = fraction
        self.type = token_type