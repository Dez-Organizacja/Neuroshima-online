# import requests
# from pathlib import Path
# import json

# base_url = "http://127.0.0.1:5000/api/neuroshima"
# def test():
#     current_dir = Path(__file__).parent
#     path = current_dir / "data.json"
#     with open(path, "r") as file:
#         data = json.load(file)
    
#     # print(data)
#     post_data = requests.post(f"{base_url}/action", json=data).json()
#     print(post_data)

# test()