import os
import glob
import pandas as pd

os.chdir(os.getcwd() + '/Data/2011-2020/')

files = [i for i in glob.glob('*.{}'.format('csv'))]

files.sort()

combined_csv = pd.concat([pd.read_csv(f) for f in files ])

combined_csv.to_csv("2011-2020_officialBoxScore.csv", index=False)