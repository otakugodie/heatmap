"""
import pandas as pd
import os
import folium
import webbrowser
import branca.colormap as cm
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster



# Getting the locations and saving to a Pandas data frame
map_df_orig = pd.read_csv("ECMOBIE-HeatMap-Resume.csv")
#map_df_orig = pd.read_csv("EnergiaConsumida2022MOBIE-HeatMap.csv")
#print(map_df_orig.head())

#Keeping only the columns I need
map_df = map_df_orig[["latitude", "longitude", "energiaConsumida2022"]]
#print(map_df.head())

values = list(map_df['energiaConsumida2022'].quantile([0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
print(values)

# **************

bins = pd.cut(map_df['energiaConsumida2022'], bins=10)
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
heatmap=HeatMap(map_df, min_opacity=0.6, radius=17, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))

colormap_dept = cm.StepColormap(colors=colors, vmin=min(map_df['energiaConsumida2022']), vmax=max(map_df['energiaConsumida2022']), index=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

#colormap = folium.LinearColormap(colors, gradient, vmin=min(values), vmax=max(values))
#colormap.add_to(heatmap)
colormap_dept.add_to(map)

# Add markers with MarkerCluster
feature_group=folium.FeatureGroup(name="Postos", show=False)
marker_cluster = MarkerCluster(name="Cluster Postos", show=False).add_to(map)

#MarkerCluster
for i in range(0,len(map_df)):
    my_markers=folium.Marker(location=[map_df.iloc[i]['latitude'], map_df.iloc[i]['longitude']], popup=map_df.iloc[i]['energiaConsumida2022']).add_to(marker_cluster)
    #folium.Marker(location=[map_df.iloc[i]['latitude'], map_df.iloc[i]['longitude']], popup=map_df.iloc[i]['energiaConsumida2022']).add_to(feature_group)
    folium.Marker(location=[map_df_orig.iloc[i]['latitude'], map_df_orig.iloc[i]['longitude']], popup=str(map_df_orig.iloc[i]['ID_INTGR'])+": "+str(map_df_orig.iloc[i]['energiaConsumida2022']), icon=folium.Icon(color='lightgreen', icon='info-sign')).add_to(feature_group)
#folium.plugins.FastMarkerCluster(my_markers).add_to(map)    






feature_group.add_to(map)

folium.LayerControl().add_to(map)

map.save(os.path.join('results', 'map.html')) 


"""


import folium.plugins
import branca
import branca.colormap as cm
import os

fname = 'test_colorbar.html'
# Load Folium map object, working with Open Street Map and zoom of 17
# Note that 17-zoom is maximum possible zoom
base_lat = 50.682294344
base_lon = 10.939628989
f_map = folium.Map(location=[base_lat,base_lon], tiles="OpenStreetMap", zoom_start=17)

lat_ = [50.6823, 50.6822, 50.6821, 50.6820, 50.6819]
lon_ = [10.9396291, 10.9396279, 10.9396269, 10.9396265, 10.9396261]
acc_ = [11.0,44.5,149.9,319.1,540.0,752.6]

colormap = cm.LinearColormap(colors=['darkblue', 'blue', 'cyan', 'yellow', 'orange', 'red'],
                             index=[0, 200, 400, 600, 800, 1000], vmin=0, vmax=1000,
                             caption='Total Standard deviation at the point[mm]')

fg = folium.FeatureGroup(name=fname.split('.')[0])    

for pt in range(len(lat_)):
    color = colormap(acc_[pt])
    fg.add_child(folium.CircleMarker(location=[lat_[pt],lon_[pt]],
                                     radius=6,
                                     fill=True,
                                     color=color,
                                     fill_color=color))

f_map.add_child(fg)
f_map.add_child(colormap)
# Save the result as an HTML file
print('Saving the map file...')

f_map.save(os.path.join('results', 'map.html')) 
