import requests
import json

base_url = "http://127.0.0.1:5000/api/neuroshima"
post_data = {
    "fractions" : ["moloch", "borgo"],
}

post_data = requests.post(f"{base_url}/", json=post_data).json()
print(post_data)
# post_data = zapytaj({"type" : "hand", "slot" : 0}, post_data)
# post_data = zapytaj({"type" : "board", "x" : 2, "y" : 0}, post_data)
# post_data = zapytaj({"type" : "rotate", "x" : 2, "y" : 0, "rotation" : 1}, post_data)
# post_data = zapytaj({"type" : "button", "button" : "end_turn"}, post_data)

# post_data = zapytaj({"type" : "hand", "slot" : 0}, post_data)
# post_data = zapytaj({"type" : "board", "x" : 2, "y" : 4}, post_data)
# post_data = zapytaj({"type" : "rotate", "x" : 2, "y" : 4, "rotation" : 5}, post_data)
# post_data = zapytaj({"type" : "button", "button" : "end_turn"}, post_data)
