# -*- coding: utf-8 -*-
"""
Created on Tue May  9 20:40:44 2023

This module uses the AEMO projections and creates a choropleth
graph according to MLF values using the folium package

@author: LIY1
"""
import geopandas as gpd
import pandas as pd
import folium
import osmnx as ox

def mlf_chloropleth(state,m):
    mlf_file = r'C:\Users\liy1\OneDrive - Jacobs\Projects\0 Training\5 OpenStreetMap\mlf.xlsx'
    # Read in the MLF project data
    if state == 'NSW':
        df = pd.read_excel(mlf_file, 'NSW')
    elif state == 'QLD':
        df = pd.read_excel(mlf_file, 'QLD')
    elif state == 'VIC':
        df = pd.read_excel(mlf_file, 'VIC')
    elif state == 'SA':
        df = pd.read_excel(mlf_file, 'SA')
    elif state == 'TAS':
        df = pd.read_excel(mlf_file, 'TAS')
    
    # In order to create a chloropleth, we need two things:
    # 1. A set of geographic regions and their boundary coordinates
    # 2. A numeric value for each region, used for the color
    
    # Create a geodataframe with region geometries from the mlf nodes
    gdf = gpd.GeoDataFrame()
    mlf_df = pd.DataFrame()
    nodes = []
    mlfs = []
    for row in df.iterrows():
        node = str(row[1][0]) + ', ' + state + ', AU'
        try:
            geom = ox.geocode_to_gdf(node)
        except ValueError:
            continue
        gdf = pd.concat([gdf, geom])
        nodes.append(str(row[1][0]))
        mlfs.append((row[1][3]))
    
    # Include ACT MLF values if state is NSW
    # if state == 'NSW':
    #     df = pd.read_excel(mlf_file, 'ACT')
    #     for row in df.iterrows():
    #         node = str(row[1][0]) + ', ' + 'ACT' + ', AU'
    #         try:
    #             geom = ox.geocode_to_gdf(node)
    #         except ValueError:
    #             continue
    #         gdf = pd.concat([gdf, geom])
    #         nodes.append(str(row[1][0]))
    #         mlfs.append((row[1][3]))
            
    # Create dataframes and geojson for choropleth making
    mlf_df['Node'] = nodes
    mlf_df['MLF'] = mlfs
    gdf['Node'] = nodes
    gdf['MLF'] = mlfs
    
    gdf = gdf.to_json()

    folium.Choropleth(geo_data=gdf,
                      name="choropleth",
                      data=mlf_df,
                      columns=["Node", "MLF"],
                      key_on='feature.properties.Node',
                      fill_color="YlOrRd",
                      fill_opacity=0.7,
                      line_opacity=0.1,
                      legend_name='MLF Values',
                      ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    # Add hover functionality
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    
    hover = folium.features.GeoJson(data = gdf,
                                    style_function=style_function, 
                                    control=False,
                                    highlight_function=highlight_function, 
                                    tooltip=folium.features.GeoJsonTooltip(fields=['Node','MLF'],
                                                                           aliases=['Node','MLF'],
                                                                           style=("background-color: white; color: #333333; font-size: 12px; padding: 10px") 
                                                                           )
                                    )   
    m.add_child(hover)
    m.keep_in_front(hover)
    
    return m


