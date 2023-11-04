import json
import os

body=""
target = os.path.join(os.getcwd(), "config.json")
print(target)
with open(target, 'r') as f:
    body = f.read()

data = json.loads(body)
print(f"body : {body}\ndata : {data}")

print("TEST #1")