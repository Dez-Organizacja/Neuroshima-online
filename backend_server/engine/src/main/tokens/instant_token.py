# from main.utils.variable import *
# from main.tokens.abstract_token import Token
# from main.tokens.data import Ability, TokenType, TokenKey
# from main.state.serialization import Serializator
# import main.frakcje.wszystkie_frakcje as allfractions
# from dataclasses import dataclass, field

# @dataclass
# class InstantToken(Token):
    

    # def __post_init__(self):
    #     faction_config = allfractions.frakcje.get(self.faction, {})
    #     token = faction_config.get(self.name, {})
    #     self.abilities.ability = token.get(TokenKey.ABILITY, Ability.NO_ABILITY)