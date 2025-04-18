import json

with open("firebase_key.json") as f:
    data = json.load(f)
    print(data["private_key"].replace("\n", "\\n"))
