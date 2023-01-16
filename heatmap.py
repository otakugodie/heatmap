import pandas as pd
import os
import folium
import webbrowser
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from branca.colormap import linear
from branca.colormap import StepColormap


# Getting the locations and saving to a Pandas data frame
#map_df_orig = pd.read_csv("ECMOBIE-HeatMap-Resume.csv")
map_df_orig = pd.read_csv("EnergiaConsumida2022MOBIE-HeatMap.csv")

#Keeping only the columns I need
map_df = map_df_orig[["latitude", "longitude", "energiaConsumida2022"]]

values = list(map_df['energiaConsumida2022'].quantile([0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
#print(values)

# **************
#bins = pd.cut(map_df['energiaConsumida2022'], bins=10)
#print(bins)

# Assign colors to each bin
colors = ['#1e51ff', '#00c800', '#00ff00', '#80ff00', '#ffff00', '#f8ba00', '#ff9d00', '#ff8000', '#ff4000', '#ff0000']

# Create a dictionary to define the gradient
#gradient = dict(zip(bins, colors))



# Create a dictionary to define the gradient
#gradient = bins.map(dict(zip(bins.unique(),colors)))
#gradient={1: '#1e51ff', 13172: '#00c800', 26344: '#00ff00', 39515: '#80ff00', 52687:  '#ffff00', 65859: '#f8ba00', 79031: '#ff9d00', 92203: '#ff8000', 105374: '#ff4000', 118543: '#ff0000'}
gradient={0.1: '#1e51ff', 0.2: '#00c800', 0.3: '#00ff00', 0.4: '#80ff00', 0.5:  '#ffff00', 0.6: '#f8ba00', 0.7: '#ff9d00', 0.8: '#ff8000', 0.9: '#ff4000', 1: '#ff0000'}


# **************



#Creating the map
map = folium.Map(location=[map_df.latitude.mean(), map_df.longitude.mean()], zoom_start=7, tiles='OpenStreetMap', control_scale=True)

#HeatMap(map_df, min_opacity=0.6, radius=17, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))
#HeatMap(map_df, gradient=gradient, min_opacity=0.5, overlay=True, control=False, show=True)

#HeatMap(map_df, min_opacity=0.6, radius=17, gradient=gradient, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))
#heatmap=HeatMap(map_df, min_opacity=0.6, radius=17, gradient=gradient, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))
heatmap=HeatMap(map_df, min_opacity=0.4, radius=17, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))
#colormap = folium.LinearColormap(colors, gradient, vmin=min(values), vmax=max(values))
#colormap = StepColormap(["blue", "yellow", "red"], index=[min(map_df['energiaConsumida2022']), 10, max(map_df['energiaConsumida2022'])], vmin=min(map_df['energiaConsumida2022']), vmax=max(map_df['energiaConsumida2022']),tick_labels=[min(map_df['energiaConsumida2022']), 65859, max(map_df['energiaConsumida2022'])])
colormap = StepColormap(colors=colors, index=[min(map_df['energiaConsumida2022']), 13172, 26344, 39515, 52687, 65859, 79031, 92203, 105374, max(map_df['energiaConsumida2022'])], vmin=min(map_df['energiaConsumida2022']), vmax=max(map_df['energiaConsumida2022']),tick_labels=[min(map_df['energiaConsumida2022']), 13172, 26344, 39515, 52687, 65859, 79031, 92203, 105374, max(map_df['energiaConsumida2022'])] )                                                                                                                                       
colormap.add_to(map)

# Add markers with MarkerCluster
feature_group=folium.FeatureGroup(name="Postos", show=False)
marker_cluster = MarkerCluster(name="Cluster Postos", show=False).add_to(map)

#MarkerCluster
for i in range(0,len(map_df)):
    my_markers=folium.Marker(location=[map_df.iloc[i]['latitude'], map_df.iloc[i]['longitude']], popup=map_df.iloc[i]['energiaConsumida2022']).add_to(marker_cluster)    
    folium.Marker(location=[map_df_orig.iloc[i]['latitude'], map_df_orig.iloc[i]['longitude']], popup=str(map_df_orig.iloc[i]['ID_INTGR'])+": "+str(map_df_orig.iloc[i]['energiaConsumida2022']), icon=folium.Icon(color='lightgreen', icon='info-sign')).add_to(feature_group)

feature_group.add_to(map)
folium.LayerControl().add_to(map)

map.save(os.path.join('results', 'HeatmapPortugal.html')) 