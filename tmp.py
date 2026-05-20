import requests

BASE_URL = "http://localhost:8080"

def login(username, password):
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": username, "password": password}
    )

    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Login failed:", response.json())
        return None


token = login("player1", "player1")

if token:
    print("Logged in! Token:", token)
