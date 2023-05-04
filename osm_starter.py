# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 18:14:17 2023

This is a starting script for using python to access OpenStreetMap

@author: LIY1
"""
# %% Importing libraries
import os
import requests
import json
import folium
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import webbrowser

#  Start timer
start = time.time()

# %% Overpass API query
overpass_url = "https://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["ISO3166-2"="AU-NSW"][admin_level=4];
(
  node(area)["power"];
  way(area)["power"];
  rel(area)["power"];
);
out body;
"""
  # way(area)["power"];
  # relation(area)["power"];
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

# %% Data processing
# Create datraframe to store nodes from OSM
df = pd.DataFrame()
coords = []
names = []
types = []
lats = []
lons = []

for element in data['elements']:
    if element['type'] == 'node' or element['type'] == 'way' or element['type'] == 'rel':
        tags = element['tags']
        lat = element['lat']
        lon = element['lon']
        type = tags['power']
        lats.append(lat)
        lons.append(lon)
        coords.append((lon,lat))
        types.append(type)
                              
        if 'name' in tags:
            name = tags['name']
        else:
            name = 'Unknown'
        
        names.append(name)
        
    elif 'centre' in element:
        tags = element['tags']
        lat = element['center']['lat']
        lon = element['center']['lon']
        type = element['power']
        lats.append(lat)
        lons.append(lon)
        coords.append((lon,lat))
        types.append(type)
        
        if 'name' in tags:
            name = tags['name']
        else:
            name = 'Unknown'            
        
        name.append(name) 

df['Name'] = names
df['Latitude'] = lats
df['Longitude'] = lons
df['Type'] = types

# Create a map centered on New South Wales
m = folium.Map(location=[df.Latitude.mean(), df.Longitude.mean()],
                 zoom_start=6, control_scale=True)
# Define marker colors for different types
type_colour = {'substation':'red', 'line':'green'}

# Loop through each row in the dataframe
for i,row in df.iterrows():
    # Setup the content of the popup
    iframe = folium.IFrame('Name:' + str(row["Name"]))
    
    # Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    
    try:
        icon_color = type_colour[row['Type']]
    except:
        # Catch nans
        icon_color = 'gray'
    
    # Add each row to the map
    folium.Marker(location=[row['Latitude'],row['Longitude']],
                  popup = popup, 
                  icon=folium.Icon(color=icon_color, icon='cloud')).add_to(m)    
                      
    #     voltage = tags.get('voltage', 'Unknown')
    #     if voltage != 'Unknown':
    #         voltage = voltage.replace('kV', '').strip()
    #         voltage = float(voltage)
    # else:
    #     continue


    # if 'power' in tags and tags['power'] == 'substation':
    #     folium.Marker([lat, lon], tooltip=tooltip).add_to(m)
    # elif 'power' in tags and tags['power'] == 'line':
    #     if voltage != 'Unknown':
    #         color = 'red' if voltage > 66 else 'blue'
    #         folium.PolyLine([(n['lat'], n['lon']) for n in element['geometry']], color=color).add_to(m)

# %% Plot output in matplotlib          
X = np.array(coords)
plt.plot(X[:, 0] , X[:, 1], '.')
plt.title('Power infrastructure NSW')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('equal')
plt.show()

# %% Save output files
# Save the map to an HTML file
m.save('substations_and_lines.html')
# webbrowser.open('substations_and_lines.html', new=2)

# Define the current working folder
working_folder = os.getcwd()
writer = pd.ExcelWriter(working_folder + '\power_coordinates.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'coords', index=False)
writer.close()

# End timer
end = time.time()
print("Done! Took %d minutes, %d seconds" %(((end - start)/60),(end - start)%60))
