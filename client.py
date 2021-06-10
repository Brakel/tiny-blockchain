import requests
import json


mine_url = "http://localhost:5000/mine"
tx_url = "http://localhost:5000/tx"

r1 = requests.post(
    tx_url,
    '{"sender": "Whale", "recipient": "Hodler", "amount": 20}',
    headers={"Content-Type": "application/json"},
)
r2 = requests.get(mine_url)
pretty_r2 = json.loads(r2.content)
print(json.dumps(pretty_r2, indent=4))
