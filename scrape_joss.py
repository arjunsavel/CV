import pandas as pd
from gsheets import Sheets
import json
import numpy as np

import sys
import os

data = sys.argv[1]

with open('new_secret.json', 'w') as outfile:
    json.dump(data, outfile)


sheets = Sheets.from_files('new_secret.json')
os.remove(new_secret.json)

joss_reviews_id = '1PAPRJ63yq9aPC1COLjaQp8mHmEq3rZUzwUYxTulyu78'

s = sheets[joss_reviews_id]

s.sheets[0].to_csv('test.csv')

joss_table = pd.read_csv('test.csv')

my_username = 'arjunsavel'

review_col = 'Review count(last quarter)'
num_reviews = joss_table[joss_table.username==my_username][review_col].values[0]
np.savetxt('num_joss_reviews.txt', [num_reviews])
