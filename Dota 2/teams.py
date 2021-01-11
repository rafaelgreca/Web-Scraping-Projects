import requests
import pandas as pd
import json

teams = requests.get('https://api.opendota.com/api/teams')

with open('Dota2_Teams.json', 'w', encoding='utf-8') as f:
    json.dump(teams.json(), f, ensure_ascii=True, indent=4)

df = pd.read_json('Dota2_Teams.json')
df.to_csv("Dota2_Teams.csv", index=False)