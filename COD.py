import os
from os import walk
from mplsoccer.pitch import Pitch
import numpy as np
import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

directory = 'DataSet/Male/Euros/Matches (2020)/Events'

# List all files in the directory
files = os.listdir(directory)

# Filter out only JSON files
json_files = [file for file in files if file.endswith('.json')]
a = 0
L = []

L = []  # List to store each game's DataFrame
for json_file in json_files:
    file_path = os.path.join(directory, json_file)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    df = pd.json_normalize(data)  # Normalize data into a DataFrame
    L.append(df)  # Append DataFrame to the list

combined_df = pd.concat(L, axis=0)  # Concatenate all DataFrames vertically














df = combined_df


print(df)


event_types = ['Pass', 'Shot']  # Define your interested event types
filtered_df = combined_df[combined_df['type.name'].isin(event_types)]

# Extract coordinates
filtered_df['x'] = filtered_df['location'].apply(lambda loc: loc[0] if isinstance(loc, list) else None)
filtered_df['y'] = filtered_df['location'].apply(lambda loc: loc[1] if isinstance(loc, list) else None)






df = df[df['location'].notna()]

# Extract X and Y coordinates
df['x'] = df['location'].apply(lambda x: x[0])
df['y'] = df['location'].apply(lambda x: x[1])


from mplsoccer import Pitch
import matplotlib.pyplot as plt

from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt


# Create a pitch
pitch = Pitch(pitch_type='statsbomb', line_color = 'black', line_zorder=2)
fig, ax = pitch.draw()


# Assuming 'df' is your DataFrame with 'x' and 'y' as columns for the locations
kdeplot = pitch.kdeplot(df['x'], df['y'], ax=ax, shade=True, levels=50, cmap='Reds')

plt.show()
