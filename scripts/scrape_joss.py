import pandas as pd
from gsheets import Sheets
import json
import numpy as np

import sys
import os

data = sys.argv[1]

sheets = Sheets.from_developer_key(data)

joss_reviews_id = '1PAPRJ63yq9aPC1COLjaQp8mHmEq3rZUzwUYxTulyu78'

s = sheets[joss_reviews_id]

s.sheets[0].to_csv('test.csv')

joss_table = pd.read_csv('test.csv')

my_username = 'arjunsavel'

review_col = 'Review count(all time)'
num_reviews = int(joss_table[joss_table.username==my_username][review_col].values[0])
np.savetxt('../data/num_joss_reviews.txt', [num_reviews])
