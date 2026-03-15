import requests
import json

url = "http://localhost:8080/api/math/"

with open("test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

response = requests.post(url, json=data)

# print(response.status_code)
print(response.text)