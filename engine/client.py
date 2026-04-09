import requests
import json

base_url = "http://127.0.0.1:5000/api/neuroshima"

def zapytaj(action, post_data):
    if(action is not None):
        post_data["action"] = action
    # if(len(action) > 0):
    #     post_data["user_actions"].append(actions)

    post_data = requests.post(f"{base_url}/click", json=post_data).json()
    # print("POST response:", post_data)
    # print("\n---------------------------\n")
    return post_data

post_data = {
    "faza" : "newgame",
    "frakcje" : {"player1": "moloch", "player2": "borgo"},
}



post_data = requests.post(f"{base_url}/newgame", json=post_data).json()

post_data = zapytaj({"type" : "hand", "slot" : 0}, post_data)
post_data = zapytaj({"type" : "board", "x" : 2, "y" : 0}, post_data)
post_data = zapytaj({"type" : "rotate", "x" : 2, "y" : 0, "rotation" : 1}, post_data)
post_data = zapytaj({"type" : "bottom", "bottom" : "end_turn"}, post_data)

post_data = zapytaj({"type" : "hand", "slot" : 0}, post_data)
post_data = zapytaj({"type" : "board", "x" : 2, "y" : 4}, post_data)
post_data = zapytaj({"type" : "rotate", "x" : 2, "y" : 4, "rotation" : 5}, post_data)
post_data = zapytaj({"type" : "bottom", "bottom" : "end_turn"}, post_data)
