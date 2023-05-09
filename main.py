# -*- coding: utf-8 -*-
"""
Created on Fri May  5 00:55:46 2023

This the main file for visualising power system data from OSM,
using the osmnx module, folium, and matplotlib.

@author: LIY1
"""
# Import libraries
import folium
import time
import osmnx as ox
from gdf2map import *
from gdf2plot import *
from mlf_chloropleth import *

# Start timer
start = time.time()

# Specify the place that is used to seach for the data
place_name = 'Sydney, NSW, AU'
# Input the state for mlf projections
state = 'NSW'

# Get centre coordinates of place
centre = ox.geocode_to_gdf(place_name).centroid
centre_lon = centre[0].x
centre_lat = centre[0].y

# Extract OSM data and create a geodataframe with NSW power infrastructure
substation_tags = {'power':'substation'}   
substations = ox.geometries_from_place(place_name, substation_tags)
line_tags = {'power':'line'}   
lines = ox.geometries_from_place(place_name, line_tags)
gen_tags = {'power':'generator'}
gens = ox.geometries_from_place(place_name, gen_tags)

# Create a folium map
m = folium.Map(location=[centre_lat,centre_lon],
                 zoom_start=12, control_scale=True)

# Call function to add power infrastructure to map
m = gdf2map(substations,m)
m = gdf2map(lines,m)
m = gdf2map(gens,m)

# Call the function to create a choropleth on map
m, mlf_df =  mlf_chloropleth(state,m)

# Save to .html file in working folder
m.save('subs.html')

# End timer
end = time.time()
print('Done! Took %d minutes, %d seconds' %(((end - start)/60),(end - start)%60))