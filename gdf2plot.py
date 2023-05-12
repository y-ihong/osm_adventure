# -*- coding: utf-8 -*-
"""
Created on Tue May  9 13:04:21 2023

This module plots the geometries of geodataframes from osmnx into a simple plot
using matplotlib and cartopy, with OSM basemap

@author: LIY1
"""
# Import libraries
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import io
from urllib.request import urlopen, Request
from PIL import Image


# This function pretends not to be a Python script
def image_spoof(self, tile): 
    url = self._image_url(tile) # get the url of the street map API
    req = Request(url) # start request
    req.add_header('User-agent','Anaconda 3') # define the user agent
    fh = urlopen(req) 
    im_data = io.BytesIO(fh.read()) # get image
    fh.close() # close url
    img = Image.open(im_data) # open image with PIL
    img = img.convert(self.desired_tile_form) # set image format
    return img, self.tileextent(tile), 'lower' # reformat for cartopy

def gdf2plot(df1,df2,df3,centre_lat,centre_lon):
    # Call image_spoofing and reformat web request for street map spoofing
    cimgt.OSM.get_image = image_spoof 
    # Spoofed, downloaded street map
    osm_img = cimgt.OSM() 
    
    fig = plt.figure(figsize=(12,9)) # open matplotlib figure 
    # Project using coordinate reference system (CRS) of street map
    ax = plt.axes(projection=osm_img.crs) 
    center_pt = [centre_lat, centre_lon] # lat/lon of centre of map display
    zoom = 4 # for zooming out of center point
    extent = [center_pt[1]-(zoom*2.0),center_pt[1]+(zoom*2.0),center_pt[0]-zoom,center_pt[0]+zoom] # adjust to zoom
    ax.set_extent(extent) # set extents

    scale = np.ceil(-np.sqrt(2)*np.log(np.divide(zoom,350.0))) # empirical solve for scale based on zoom
    scale = (scale<20) and scale or 19 # scale cannot be larger than 19
    ax.add_image(osm_img, int(scale)) # add OSM with zoom specification
    
    ax.add_geometries(df1.geometry, crs=ccrs.PlateCarree(), edgecolor='blue', facecolor='none', linewidth=2)
    ax.add_geometries(df2.geometry, crs=ccrs.PlateCarree(), edgecolor='green', facecolor='none', linewidth=2)
    ax.add_geometries(df3.geometry, crs=ccrs.PlateCarree(), edgecolor='red', facecolor='none', linewidth=1)
    
    ax.annotate('You are here', xy=(0,0), xycoords='figure pixels',
                xytext=(0, 0), textcoords='offset pixels',
                arrowprops=dict(facecolor='black', shrink=0.1),
                horizontalalignment='right', verticalalignment='bottom')
    # if type == 'substation':
    #     ax.plot([lon], [lat],
    #               color='blue', marker='.',
    #               )
    # elif type == 'generator':
    #     ax.plot([lon], [lat],
    #               color='green', marker='.',
    #               )
         
    # Plot output in matplotlib   
    plt.title('Power infrastructure in area')
    plt.legend()    
    plt.show() # show the plot
    
    return
    