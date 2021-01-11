import requests
import pandas as pd
import json
import os
import glob

last_match = ''
url = 'https://api.opendota.com/api/proMatches'

for i in range(0, 200):
    
    if last_match != '':
        url = url + '?less_than_match_id=' + last_match
    
    pro_matches = requests.get(url)
    print(pro_matches)
    last_match = str(pro_matches.json()[len(pro_matches.json())-1]['match_id'])
    
    with open('Dota2_ProMatches'+str(i)+'.json', 'w', encoding='utf-8') as f:
        json.dump(pro_matches.json(), f)

    df = pd.read_json('Dota2_ProMatches'+str(i)+'.json')
    df.to_csv("Dota2_ProMatches"+str(i)+".csv", index=False)

os.chdir(os.getcwd())
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
all_filenames = list(reversed(all_filenames))

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
#export to csv
combined_csv.to_csv("Dota2_ProMatches.csv", index=False, encoding='utf-8-sig')