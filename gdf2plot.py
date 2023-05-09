# -*- coding: utf-8 -*-
"""
Created on Tue May  9 13:04:21 2023

This module plots the geometries of geodataframes from osmnx into a simple plot
using matplotlib and cartopy

@author: LIY1
"""
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
# import cartopy.crs as ccrs


def gdf2plot(df):
    # Initialise lists
    coords = []
    names = []
    types = []
    lats = []
    lons = []
    
    # Display basemap
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
            
    for row in df.iterrows():
        if row[0][0] == 'node':
            name = row[1]['name']
            lat = row[1]['geometry'].y
            lon = row[1]['geometry'].x
            type = row[1]['power']
            


            plt.plot([lon], [lat],
                     color='blue', marker='o',
                     transform=ccrs.Geodetic(),
                     )
            
            
        elif row[0][0] == 'way' or row[0][0] == 'relation':
            continue
    
    
    
    # Plot output in matplotlib          \
    plt.title('Power infrastructure NSW')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()