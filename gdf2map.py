# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:48:44 2023

This module returns the names and geometries of nodes, ways, and relations 
of a geodataframe from osmnx as a plot for a map

@author: LIY1
"""
# Import libraries
import folium
import geopandas as gpd
import pandas as pd

def gdf2map(df,m):
   
    # Iterate through the rows of the geodataframe
    for row in df.iterrows():
        # Determine the style function based on the object
        if 'substation' in row[1]:
            style_function=lambda x: {'fillColor': 'blue',
                                      'color':'blue',
                                      'weight':2}
        elif 'generator:type' in row[1]:
            style_function=lambda x: {'fillColor': 'green',
                                      'color':'green',
                                      'weight':2}
        # Determine line color based on the line voltage
        elif 'line' in row[1]:
            # Check for NaN values and convert string to integer
            # if pd.isnull(row[1]['voltage']) != True or row[1]['voltage'] != 'unknown':
            #     if ';' in str(row[1]['voltage']):
            #         voltage = 66000
            #     else:
            try:
                voltage = int(row[1]['voltage'])
            except ValueError or TypeError:
                voltage = 66000
                
            if voltage >= 11000 and voltage < 66000:
                style_function=lambda x: {'fillColor': 'orange',
                                          'color':'orange',
                                          'weight':1}
            elif voltage >= 66000 and voltage < 132000:
                style_function=lambda x: {'fillColor': 'red',
                                          'color':'red',
                                          'weight':1}
            elif voltage >= 132000 and voltage < 330000:
                style_function=lambda x: {'fillColor': 'purple',
                                          'color':'purple',
                                          'weight':1}
            elif voltage >= 330000 and voltage <= 500000:
                style_function=lambda x: {'fillColor': 'black',
                                          'color':'black',
                                          'weight':1}
            else:
                style_function=lambda x: {'fillColor': 'yellow',
                                          'color':'yellow',
                                          'weight':1}
            
        # Setup the content of the popup
        try:
            name = str(row[1]['name'])
        except KeyError:
            name = 'Unknown'
        
        iframe = folium.IFrame('Name:' + name)
        
        # Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300)   
                
        if row[0][0] == 'node':            
            # Add each row to the map by extracting coordinates from shapely point
            # folium.Marker(location=[row[1]['geometry'].xy[1][0],row[1]['geometry'].xy[0][0]], 
            #               popup=popup, icon=folium.Icon(icon='cloud')).add_to(m)
            folium.GeoJson(data=row[1]['geometry'],popup=popup,
                           marker=folium.CircleMarker(radius = 2),
                           style_function=style_function).add_to(m) 
            
        elif row[0][0] == 'way' or row[0][0] == 'relation':           
            # Add each row to the map by extracting coordinates from shapely polygon
            # Without simplifying, the map might not be displayed
            geo = gpd.GeoSeries(row[1]['geometry']).simplify(tolerance=0.001)
            geo_j = geo.to_json()
            folium.GeoJson(data=geo_j, popup=popup, name=name,
                           style_function=style_function).add_to(m)
                    
    return m