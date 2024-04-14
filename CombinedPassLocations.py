import os
from os import walk

from mplsoccer.pitch import Pitch
import numpy as np
import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

directory = 'DataSet\\Female\\Euros\\Matches (2022)\\Events'

# List all files in the directory
files = os.listdir(directory)

# Filter out only JSON files
json_files = [file for file in files if file.endswith('.json')]
a = 0
L = []

for json_file in json_files:
    # Construct the full path to the JSON file
    file_path = os.path.join(directory, json_file)

    # Open the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the JSON data
        data = json.load(file)
    a += 1
    print(a)
    df = pd.json_normalize(data) #turn the json data into a dataframe

    austria_passes = df[(df['type.name'] == 'Pass') & (df['team.name'] == "England Women's")] #select passes and for which team

    indv_location_pass = austria_passes.location.apply(pd.Series) #get the location of where the passes took place
    indv_location_pass.columns = ['x', 'y'] #rename the columns into x and y data, theyre currently stored as a list
    indv_location_pass.dropna(inplace=True) #get rid of NaN values:
    print(indv_location_pass)
    L.append(indv_location_pass)
    combined_df = pd.concat(L, axis=1)
    location_pass = combined_df

fig, axes = plt.subplots(1, 3, figsize=(25, 10))  # Adjust the figsize as needed

for i, ax in enumerate(axes): #loop over the axes
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white', line_zorder=2) #create the pitch
    pitch.draw(ax=ax)  # Draw the pitch on the current axis
    ax.set_aspect(10/6) #change aspect ratio on figures
    bins = [(6,5), (1, 5), (6,1)] #different plots (THIS DETERMINES NO OF SQUARES IN FIGURE)
    bin_statistic = pitch.bin_statistic(location_pass.x, location_pass.y, statistic='count', bins=bins[i]) #select bin and store location for each pass
    pitch.heatmap(bin_statistic, ax=ax, cmap='coolwarm', edgecolors='#22312b') #draw heatmap
    pitch.scatter(location_pass.x, location_pass.y, c='white', s=5, ax=ax) #make a scatter plot for each pass event
    bin_statistic['statistic'] = (pd.DataFrame((bin_statistic['statistic'] / bin_statistic['statistic'].sum())).applymap(lambda  x:'{:.0%}'.format(x)).values)
    pitch.label_heatmap(bin_statistic, color='black', fontsize=11, ax=ax, ha='center', va='bottom')

plt.subplots_adjust(wspace=0.5)  #adjusts width of percentages on figure
fig.suptitle('Passes location for England Women Euros 2022', x=0.5, y=0.98, fontsize=10)

plt.show()

plt.style.use('dark_background') #choose background for heatmap

pitch = Pitch(pitch_type='statsbomb', line_color = 'white', line_zorder=2)
fig, ax = pitch.draw() #draw pitch
bin_statistic = pitch.bin_statistic(location_pass.x, location_pass.y, statistic='count', bins = (25,25))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
cbar = fig.colorbar(pcm, ax=ax)
title = fig.suptitle('Passes location for England Women Euros 2022', x=0.4, y=0.98, fontsize=23)
plt.show()