import requests
import json

base_url = "http://127.0.0.1:5000/api/neuroshima"

post_data = {
    "x": 2,
    "y": 4,
    "frakcja": "borgo",
    "nazwa": "sztab",
    "rotacja": 3
}

response = requests.post(f"{base_url}/postaw", json=post_data)
print("POST response:", response.json())

post_data = {
    "x": 1,
    "y": 3,
    "frakcja": "moloch",
    "nazwa": "rozprowacz",
    "rotacja": 2
}

response = requests.post(f"{base_url}/postaw", json=post_data)
print("POST response:", response.json())

post_data = {
    "x": 1,
    "y": 3,
    "frakcja": "moloch",
    "nazwa": "rozprowacz",
    "rotacja": 2
}

response = requests.post(f"{base_url}/postaw", json=post_data)
print("POST response:", response.json())

post_data = {
    "x": 4,
    "y": 2,
    "frakcja": "moloch",
    "nazwa": "szturmowiec",
    "rotacja": 0
}

response = requests.post(f"{base_url}/postaw", json=post_data)
print("POST response:", response.json())

response = requests.get(f"{base_url}/get_board")
print("GET response:", response.json())

print("---------------------------------------------------------------\n\n\n\n\n")
response = requests.post(f"{base_url}/bitwa")
print("GET response:", response.json())

response = requests.get(f"{base_url}/get_board")
print("GET response:", response.json())