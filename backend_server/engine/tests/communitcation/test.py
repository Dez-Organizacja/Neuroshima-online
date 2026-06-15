import requests
from pathlib import Path
import json
from main.communication.server_message import ServerMessage
from main.state.serialization import Serializator

base_url = "http://127.0.0.1:5000/api/neuroshima"
def test():
    data = {
        "factions": ["moloch", "borgo"]
    }

    post_data = requests.post(f"{base_url}", json=data).json()

    message = ServerMessage(
        messageType="GAMEVIEW_REQUEST",
        timestamp="2026-06-11T23:13:59.107120696",
        gameState=post_data,
    )

    payload = Serializator.to_dict_dataclass(message)

    post_data2 = requests.post(f"{base_url}/view", json=payload)

    print(post_data2.json())
    assert False
test()

