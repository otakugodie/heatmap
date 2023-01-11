import pandas as pd
import os
import folium
import numpy as np
from folium.plugins import HeatMap
from sklearn.preprocessing import MinMaxScaler


# Getting the locations and saving to a Pandas data frame
map_df = pd.read_csv("EnergiaConsumida2022MOBIE-HeatMap.csv")
#print(map_df.head())

#Keeping only the columns I need
map_df = map_df[["latitude", "longitude", "energiaConsumida2022"]]

scaler = MinMaxScaler()
scaler.fit(map_df[['energiaConsumida2022']])
map_df[['energiaConsumida2022']] = scaler.transform(map_df[['energiaConsumida2022']])

# Sample dataframe
map_df = pd.DataFrame(map_df, columns=["latitude", "longitude", "energiaConsumida2022"])
print(map_df)

# Create bins using pd.cut
bins = pd.cut(map_df['energiaConsumida2022'], bins=10)

# Assign colors to each bin
colors = ['#1e51ff', '#00c800', '#00ff00', '#80ff00', '#ffff00', '#f8ba00', '#ff9d00', '#ff8000', '#ff4000', '#ff0000']

# Create a dictionary to define the gradient
gradient = list(bins.map(dict(zip(bins.unique(),colors))))
#print(gradient)



map_df["energiaConsumida2022"] = pd.cut(map_df["energiaConsumida2022"], 10, labels=colors)



#Creating the map
map = folium.Map(location=[map_df.latitude.mean(), map_df.longitude.mean()], zoom_start=7, tiles='OpenStreetMap', control_scale=True)

# Create heatmap layer
heatmap = HeatMap(map_df, gradient=gradient, min_opacity=0.5, overlay=True, control=False, show=True)

heatmap.add_to(map)

map.save("map.html")