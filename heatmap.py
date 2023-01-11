import pandas as pd
import os
import folium
from folium.plugins import HeatMap


# Getting the locations and saving to a Pandas data frame
map_df = pd.read_csv("EnergiaConsumida2022MOBIE-HeatMap.csv")
#print(map_df.head())

#Keeping only the columns I need
map_df = map_df[["latitude", "longitude", "energiaConsumida2022"]]


# **************

bins = pd.cut(map_df['energiaConsumida2022'], bins=10)
#print(bins)

# Assign colors to each bin
#colors = ['#1e51ff', '#00c800', '#00ff00', '#80ff00', '#ffff00', '#f8ba00', '#ff9d00', '#ff8000', '#ff4000', '#ff0000']

# Create a dictionary to define the gradient
#gradient = dict(zip(bins, colors))



# Create a dictionary to define the gradient
#gradient = bins.map(dict(zip(bins.unique(),colors)))
#gradient={1: '#1e51ff', 13172: '#00c800', 26344: '#00ff00', 39515: '#80ff00', 52687:  '#ffff00', 65859: '#f8ba00', 79031: '#ff9d00', 92203: '#ff8000', 105374: '#ff4000', 118543: '#ff0000'}
gradient={0.1: '#1e51ff', 0.2: '#00c800', 0.3: '#00ff00', 0.4: '#80ff00', 0.95:  '#ffff00', 0.96: '#f8ba00', 0.97: '#ff9d00', 0.98: '#ff8000', 0.99: '#ff4000', 1: '#ff0000'}


# **************



#Creating the map
map = folium.Map(location=[map_df.latitude.mean(), map_df.longitude.mean()], zoom_start=7, tiles='OpenStreetMap', control_scale=True)


#HeatMap(map_df, min_opacity=0.6, radius=17, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))
#HeatMap(map_df, gradient=gradient, min_opacity=0.5, overlay=True, control=False, show=True)


#HeatMap(map_df, min_opacity=0.6, radius=17, gradient=gradient, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))
heatmap=HeatMap(map_df, min_opacity=0.6, radius=17, gradient=gradient, blur=15).add_to(folium.FeatureGroup(name='Heat Map Energia Consumida 2022').add_to(map))

"""
# Add markers
for i in range(0,len(map_df)):
    folium.Marker(location=[map_df.iloc[i]['latitude'], map_df.iloc[i]['longitude']], popup=map_df.iloc[i]['energiaConsumida2022']).add_to(map)
"""



for i, j in map_df:
    feature_group = folium.FeatureGroup(i)
    for row in j.itertuples():
        folium.Marker(location=[map_df.iloc[i]['latitude'], map_df.iloc[i]['longitude']], popup=map_df.iloc[i]['energiaConsumida2022']).add_to(feature_group)
    feature_group.add_to(mapa)



folium.LayerControl().add_to(map)



map.save(os.path.join('results', 'HeatmapPortugal.html')) 
















"""
import numpy as np 
import pandas as pd
import folium
from folium import Map
from folium.plugins import HeatMap

map_df = pd.read_csv("EnergiaConsumida2022MOBIE-HeatMap.csv", encoding = 'unicode_escape', engine ='python')

max_amount = float(map_df['energiaConsumida2022'].max())
hmap = folium.Map(location=[42.5, -75.5], zoom_start=7, )

hm_wide = HeatMap( list(zip(map_df.latitude.values, 
            map_df.longitude.values, map_df.energiaConsumida2022.values)),
                   min_opacity=0.2,
                   max_val=max_amount,
                   radius=17, blur=15, 
                   max_zoom=1, 
                 )
folium.GeoJson(district23).add_to(hmap)
hmap.add_child(hm_wide)

hmap.save(os.path.join('results', 'map.html'))


from glob import glob
import pandas as pd
import numpy as np
import os
import folium
from folium import plugins
from folium.plugins import HeatMap

#lon, lat = -86.276, 30.935 
#zoom_start = 5


data = (
    np.random.normal(size=(100, 3)) *
    np.array([[1, 1, 1]]) +
    np.array([[39, -9, 1]])
).tolist()

m = folium.Map([39.311, -8.967], tiles='stamentoner', zoom_start=7)



HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))


folium.LayerControl().add_to(m)

m.save(os.path.join('results', 'Heatmap.html')) 


import os
from glob import glob
import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap

lon, lat = -86.276, 30.935 
zoom_start = 5


data = (
    np.random.normal(size=(100, 3)) *
    np.array([[1, 1, 1]]) +
    np.array([[48, 5, 1]])
).tolist()
m = folium.Map([48, 5], tiles='stamentoner', zoom_start=6)

HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
folium.LayerControl().add_to(m)

m.save(os.path.join('results', 'Heatmap2.html')) 

"""