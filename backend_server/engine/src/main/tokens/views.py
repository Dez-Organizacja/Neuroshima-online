# def to_dict(self) -> dict:
#         data = {
#             "name": self.name,
#             "faction": self.faction,
#             "hp": self.hp,
#             "rotation": self.rotation,
#             "damage": self.damage,
#             "wounds": self.wounds,
#             "wired": self.wired,
#             "abilities" : Serializator.to_dict_dataclass(self.abilities),
#         }
#         return data
# from dataclasses import dataclass
# from main.tokens.config import Abilities

# @dataclass
# class TokenView:
#     name : str
#     faction : str
#     damage : int
#     wounds : int
#     rotation : list[int]
#     wired : bool
#     abilities : Abilities