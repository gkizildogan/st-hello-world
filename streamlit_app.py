import streamlit as st

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 21:01:46 2023

@author: Goksu
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

url = "http://www.koeri.boun.edu.tr/scripts/lst1.asp"

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

z = soup.prettify()
big_string = str(soup.find("pre").find(text=True))

word = "Niteliği"
index = big_string.find(word)
big_string = big_string[index + len(word):]

# Use a regular expression to split the big string into rows
rows = re.split(r'\n', big_string)
rows = rows[2:]
# Use a regular expression to extract the columns from each row string
column_lists = [re.findall(r'(\S+)\s+', row) for row in rows]

# Filter out any empty lists (rows)
column_lists = [cols for cols in column_lists if len(cols) == 11]

# Create a DataFrame from the list of columns
columns = ["Date", "Time", "Latitude(N)", "Longitude(E)", "Depth(km)", "MD", "ML", "Mw", "Place", "City", "Assessment"]
df = pd.DataFrame(column_lists, columns=columns)

#Magnitudes have this "not existing" symbol in the website
df = df.replace("-.-", np.nan)

# Removing parentheses.
df["City"] = df["City"].str.replace(r'[^(]*\(|\)[^)]*', '', regex=True)

df["Assessment"] = df["Assessment"].replace("İlksel", "Primary")
df.insert(0, "Timestamp", value=pd.to_datetime(df["Date"] + " " + df["Time"]))

df = df.drop(columns=["Date", "Time"])
print(df.head())
#df.to_csv("temp_data_df.csv", index=False)

