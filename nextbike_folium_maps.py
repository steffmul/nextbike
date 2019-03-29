#!/usr/bin/env python
# coding: utf-8

# In[1]:


import folium, json, requests
from folium import plugins
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
import selenium.webdriver


# In[2]:


def make_base_map(custom_map):
    custom_map = folium.Map(location=[52.510008, 13.404954],
                    zoom_start=12)
    return custom_map


# In[3]:


def add_flexzone(custom_map):
    with open(r'C:\Users\steff\Documents\DataScience Bootcamp\Bike\geo\flexzone_bn.json') as f:
        bln_zone = json.load(f)
    # add the polgon of the berlin flexzone
    folium.GeoJson(
            bln_zone,
            name='geojson'
            ).add_to(custom_map)
    return custom_map


# In[4]:


bikemap = add_flexzone(make_base_map('bikemap'))


# In[5]:


# berlin nextbike stations
url = 'https://api.nextbike.net/maps/nextbike-live.json?city=362'
response = requests.get(url).json()
with open('stations.json', 'w') as outfile:
    json.dump(response, outfile)


# In[6]:


with open(r'C:\Users\steff\Documents\DataScience Bootcamp\Bike\stations.json') as f:
        json_data = json.load(f)

# extract the relevent columns
stations = []
for i in range(0,3000):
    try:
        uid = json_data['countries'][0]['cities'][0]['places'][i]['uid']
        spot = json_data['countries'][0]['cities'][0]['places'][i]['spot']
        lat = json_data['countries'][0]['cities'][0]['places'][i]['lat']
        lng = json_data['countries'][0]['cities'][0]['places'][i]['lng']
        name = json_data['countries'][0]['cities'][0]['places'][i]['name']
        data = (uid, name, spot, lat, lng)
        stations.append(data)
    except:
        continue


# In[7]:


df_stations = pd.DataFrame(stations, columns=['uid', 'name', 'spot', 'lat', 'lng' ])
df_stations = df_stations[df_stations['spot'] == True]
df_stations['icon'] = 'https://deezer.nextbike.net/4com/icons/deezer_icon_30x43.png'
#df_stations.head()


# In[8]:


for i in range(0,len(df_stations)):
    folium.Marker(
        [df_stations.iloc[i]['lat'], df_stations.iloc[i]['lng']],
        #popup=df_stations.iloc[i]['name'],
        icon=folium.features.CustomIcon(
            df_stations.iloc[i]['icon'],
            icon_size=(15,22) ),
            popup=df_stations.iloc[i]['name']
                ).add_to(bikemap)


# ### Map of all nextbike stations and flexzone

# In[9]:


bikemap


# In[10]:


df_floating = pd.DataFrame(stations, columns=['uid', 'name', 'spot', 'lat', 'lng' ])
df_floating = df_floating[df_floating['spot'] != True]
df_floating['icon'] = 'https://iconsplace.com/wp-content/uploads/_icons/ff0000/256/png/bicycle-icon-14-256.png'
#df_floating.head()


# In[11]:


for i in range(0,len(df_floating)):
    folium.Marker(
        [df_floating.iloc[i]['lat'], df_floating.iloc[i]['lng']],
        #popup=df_stations.iloc[i]['name'],
        icon=folium.features.CustomIcon(
            df_floating.iloc[i]['icon'],
            icon_size=(15,15) ),
            popup=df_floating.iloc[i]['name']
                ).add_to(bikemap)


# ### Snapshot in time of stations versus floating bikes

# In[12]:


bikemap


# ### top pick up & return stations

# In[16]:


df = pd.read_pickle('all_trips.pkl')
df.shape


# In[17]:


df['icon'] = 'https://deezer.nextbike.net/4com/icons/deezer_icon_30x43.png'
top_pickup = df.groupby(['from_station','from_lat','from_long','icon']).size().sort_values(ascending=False).head(20)
top_pickup = top_pickup.to_frame()
top_pickup = top_pickup.reset_index()


# In[18]:


top_return = df.groupby(['to_station','to_lat','to_long','icon']).size().sort_values(ascending=False).head(20)
top_return = top_return.to_frame()
top_return = top_return.reset_index()


# In[19]:


top_pickup_map = add_flexzone(make_base_map('top_pickup_map'))
for i in range(0,len(top_pickup)):
    folium.Marker(
        [top_pickup.iloc[i]['from_lat'], top_pickup.iloc[i]['from_long']],
        icon=folium.features.CustomIcon(
            top_pickup.iloc[i]['icon'],
            icon_size=(45/10*(9-i*2) ,
                       66/10*(9-i*2) )),
            popup=
                (top_pickup.iloc[i]['from_station']+
                ' trips: '+
                str(top_pickup.iloc[i,4:5][0]))
                ).add_to(top_pickup_map)

top_pickup_map


# In[20]:


top_return_map = add_flexzone(make_base_map('top_return_map'))
for i in range(0,len(top_return)):
    folium.Marker(
        [top_return.iloc[i]['to_lat'], top_return.iloc[i]['to_long']],
        icon=folium.features.CustomIcon(
            top_return.iloc[i]['icon'],
            icon_size=(45/10*(9-i*2) ,
                       66/10*(9-i*2) )),
            popup=
                (top_return.iloc[i]['to_station']+
                ' trips: '+
                str(top_return.iloc[i,4:5][0]))
                ).add_to(top_return_map)

top_return_map


# ### most used combination of stations

# In[41]:


station_combis = pd.read_pickle('station_combis.pkl')
top_station_combis = station_combis.nlargest(30, 'cnt')
top_station_combis.shape


# In[42]:


def get_bearing(p1, p2):  
    '''
    Returns compass bearing from p1 to p2
    Based on https://gist.github.com/jeromer/2005586
    '''
    long_diff = np.radians(p2[1] - p1[1])
    
    lat1 = np.radians(p1[0])
    lat2 = np.radians(p2[0])
    
    x = np.sin(long_diff) * np.cos(lat2)
    y = (np.cos(lat1) * np.sin(lat2) 
        - (np.sin(lat1) * np.cos(lat2) 
        * np.cos(long_diff)))

    bearing = np.degrees(np.arctan2(x, y))
    
    # adjusting for compass bearing
    if bearing < 0:
        return bearing + 360
    return bearing


# In[43]:


def get_arrows(start, end , color='blue', size=6, n_arrows=1):  
    """
    Returns arrow as a polygon
    Based on https://medium.com/@bobhaffner/folium-lines-with-arrows-25a0fe88e4e
    """
    # creating start end end point 
    p1 = (start[0], start[1])
    p2 = (end[0], end[1])
    # normal rotation towards 
    rotation = get_bearing(p1, p2) - 90
    # arrow created with an polygon marker
    arrows = []
    arrows.append(folium.RegularPolygonMarker(location=p2, 
                      fill_color=color, number_of_sides=3,
                      opacity=0.3, color=color,
                      radius=size, rotation=rotation).add_to(stationmap))
    return arrows


# In[44]:


stationmap = add_flexzone(make_base_map('stationmap'))
for i in range(0,len(top_station_combis)):   
    get_arrows((top_station_combis.iloc[i]['from_lat'],
                                top_station_combis.iloc[i]['from_long']),
                                (top_station_combis.iloc[i]['to_lat'],
                                top_station_combis.iloc[i]['to_long']),
                size=(50-i)/4
    )


# In[45]:


for i in range(0,len(top_station_combis)):
    folium.PolyLine(locations=([top_station_combis.iloc[i]['from_lat'] ,
                                top_station_combis.iloc[i]['from_long']],
                               [top_station_combis.iloc[i]['to_lat'] ,
                                top_station_combis.iloc[i]['to_long']]),
                    opacity = 0.5,
                    color='blue',
                    weight= 30-i,
                    popup= (top_station_combis.iloc[i]['from_station']+
                            ' to '+
                           top_station_combis.iloc[i]['to_station']+
                            ' trips: '+
                            str(top_station_combis.iloc[i]['cnt'])
                           )
                    

                ).add_to(stationmap)
stationmap


# ### Heatmap

# In[46]:


stations = station_combis[['from_lat', 'from_long']][station_combis['from_station_mode'] == 'station']
floating = station_combis[['from_lat', 'from_long']][station_combis['from_station_mode'] == 'floating']


# In[47]:


heatmap_station = add_flexzone(make_base_map('heatmap_station'))

# convert to (n, 2) nd-array format for heatmap
stationArr = stations.values

# plot heatmap
heatmap_station.add_child(plugins.HeatMap(stationArr, radius=15))
heatmap_station


# In[50]:


#save maps as png
heatmap_station.save(r'maps_html/station_heatmap.html')
driver = selenium.webdriver.PhantomJS()
driver.set_window_size(800, 600)  # choose a resolution
driver.get(r'maps_html/station_heatmap.html')
# You may need to add time.sleep(seconds) here
driver.save_screenshot(r'maps_png/station_heatmap.png')


# In[51]:


heatmap_floating = add_flexzone(make_base_map('heatmap_floating'))

# convert to (n, 2) nd-array format for heatmap
floatingArr = floating.values
# plot heatmap

heatmap_floating.add_child(plugins.HeatMap(floatingArr, radius=15))
heatmap_floating


# In[52]:


#save maps as png
heatmap_floating.save(r'maps_html/floating_heatmap.html')
driver = selenium.webdriver.PhantomJS()
driver.set_window_size(800, 600)  # choose a resolution
driver.get(r'maps_html/floating_heatmap.html')
# You may need to add time.sleep(seconds) here
driver.save_screenshot(r'maps_png/floating_heatmap.png')


# ### Testing

# In[54]:


def add_biketraffic(custom_map):
    with open(r'C:\Users\steff\Documents\DataScience Bootcamp\Bike\Radverkehrsanlagen_geojson\Radverkehrsanlagen.geojson') as f:
        bln_zone = json.load(f)
    # add the polgon of the berlin flexzone
    folium.GeoJson(
            bln_zone,
            name='geojson'
            ).add_to(custom_map)
    return custom_map


# In[56]:


bikelanes = add_biketraffic(make_base_map('bikemap'))
bikelanes


# In[ ]:




