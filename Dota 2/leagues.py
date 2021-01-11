import requests
import pandas as pd
import json

leagues = requests.get('https://api.opendota.com/api/leagues')

with open('Dota2_Leagues.json', 'w', encoding='utf-8') as f:
    json.dump(leagues.json(), f, ensure_ascii=True, indent=4)

df = pd.read_json('Dota2_Leagues.json')
df.to_csv("Dota2_Leagues.csv", index=False)