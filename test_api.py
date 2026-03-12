import requests
import json

data = {"a": -1, "b": 4}

odp = requests.post(
    "http://localhost:8080/api/math/",
    headers={"Content-Type": "application/json"},
    json=data
)

odp = odp.json()

if odp is not None:
    print(json.dumps(odp, indent=4))