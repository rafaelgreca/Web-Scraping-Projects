import requests
import pandas as pd
import json

pro_players = requests.get('https://api.opendota.com/api/proPlayers')

with open('Dota2_ProPlayers.json', 'w', encoding='utf-8') as f:
    json.dump(pro_players.json(), f, ensure_ascii=True, indent=4)

df = pd.read_json('Dota2_ProPlayers.json')
df.to_csv("Dota2_ProPlayers.csv", index=False)