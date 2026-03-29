import requests
import json

base_url = "http://127.0.0.1:5000/api/neuroshima"

def zapytaj(actions, post_data):
    for action in actions:
        post_data["user_actions"].append(action)

    post_data = requests.post(f"{base_url}/click", json=post_data).json()
    print("POST response:", post_data)
    print("\n---------------------------\n")
    return post_data

post_data = {
    "faza" : "poczatek",
    "frakcje" : ["moloch", "borgo"]
}

post_data = zapytaj([], post_data)

post_data = zapytaj(["hand", 0], post_data)
post_data = zapytaj(["plansza", 2, 0], post_data)

# post_data = zapytaj([-1], post_data)
# post_data = zapytaj([1], post_data)
# post_data = zapytaj([1], post_data)
# post_data = zapytaj(["hand", 0], post_data)
post_data = zapytaj(["koniec"], post_data)
# post_data = zapytaj(["hand", 0], post_data)
post_data = zapytaj(["koniec"], post_data)

post_data = zapytaj(["hand", 0], post_data)
post_data = zapytaj(["plansza", 2, 0], post_data)
post_data = zapytaj(["hand", 0], post_data)
post_data = zapytaj(["plansza", 2, 4], post_data)
post_data = zapytaj([-1], post_data)
post_data = zapytaj(["koniec"], post_data)
post_data = zapytaj(["koniec"], post_data)

# response = requests.post(f"{base_url}/get_state", json=post_data)
# print("POST response:", response.json())
# print("\n---------------------------\n")


# post_data = response.json()
# post_data["user_actions"].append("hand")
# post_data["user_actions"].append(0)
# # print("POST DATA:", post_data)
# # print("\n---------------------------\n")

# post_data = requests.post(f"{base_url}/click", json=post_data).json()
# print("POST response:", post_data)
# print("\n---------------------------\n")

# post_data["user_actions"].append("plansza")
# post_data["user_actions"].append(2)
# post_data["user_actions"].append(0)

# post_data = requests.post(f"{base_url}/click", json=post_data).json()
# print("POST response:", post_data)
# print("\n---------------------------\n")

# post_data["user_actions"].append(1)

# post_data = requests.post(f"{base_url}/click", json=post_data).json()
# print("POST response:", post_data)
# print("\n---------------------------\n")

# post_data["user_actions"].append(1)
# post_data["user_actions"].append(-1)
# post_data = {
#     "x": 1,
#     "y": 3,
#     "frakcja": "moloch",
#     "nazwa": "rozprowacz",
#     "rotacja": 2
# }

# response = requests.post(f"{base_url}/postaw", json=post_data)
# # print("POST response:", response.json())
# # print("\n---------------------------\n")


# post_data = {
#     "x": 1,
#     "y": 3,
#     "frakcja": "moloch",
#     "nazwa": "rozprowacz",
#     "rotacja": 2
# }

# response = requests.post(f"{base_url}/postaw", json=post_data)
# # print("POST response:", response.json())
# # print("\n---------------------------\n")


# post_data = {
#     "x": 4,
#     "y": 2,
#     "frakcja": "moloch",
#     "nazwa": "szturmowiec",
#     "rotacja": 0
# }

# response = requests.post(f"{base_url}/postaw", json=post_data)
# # print("POST response:", response.json())
# # print("\n---------------------------\n")

# # response = requests.get(f"{base_url}/get_board")
# # print("GET response:", response.json())

# print("---------------------------------------------------------------\n\n\n\n\n")
# # requests.post(f"{base_url}/bitwa")

# response = requests.post(f"{base_url}/bitwa")
# print("GET response:", response.json())

# # response = requests.get(f"{base_url}/get_board")
# # print("GET response:", response.json())