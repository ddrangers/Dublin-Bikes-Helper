import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

# The bike static file will only be used for import into mysql database for one time.

# read the csv file
df = pd.read_csv("dublin1_static.csv")

print(df.shape)
print(df.head(10))
print(df.tail(10))

