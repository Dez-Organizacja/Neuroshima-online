from main.tokens.base import Token
from main.tokens.token_factory import TokenFactory
from main.state.serialization import Serializator
from main.tokens.board_token import BoardToken
import json

def execute(obj):
    cls = obj.__class__
    data = Serializator.to_dict_dataclass(obj)
    # data = obj.to_dict()
    # print(f"serialized data {data}")
    json_string = json.dumps(data)
    loaded_data = json.loads(json_string)

    # restored_token = Serializator.from_dict_dataclass(cls, loaded_data)
    restored_token = BoardToken.from_dict(loaded_data)
    # print(restored_token)

    restored_data = Serializator.to_dict_dataclass(restored_token)

    # assert False
    assert data == restored_data

# def test_instant_token():
#     token = TokenFactory.create(name="ruch", faction="moloch")
#     print(f"token instance {token}")
#     execute(token)

def test_board_token():
    token = TokenFactory.create(name="mutek", faction = "borgo")
    # print(f"token instance {token}")
    execute(token)
