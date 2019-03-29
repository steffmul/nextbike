#!/usr/bin/env python
# coding: utf-8

# In[31]:


import json
import pandas as pd
import numpy as np
from pprint import pprint
import os
from datetime import datetime


# In[32]:


def filenames(path):
    """
    get file names from json folder to derive with data and timestamp
    """
    files = os.listdir(path)
    files_lst = []
    for f in files:
        dt = (f[12:20])
        tm = (f[21:27])
        dat = (f,dt,tm)
        files_lst.append(dat)
    return(files_lst)


# In[33]:


def parse_json(file):
    with open(r'C:\Users\steff\Documents\DataScience Bootcamp\Bike\json\\'+file[0]) as f:
        json_data = json.load(f)
    return json_data


# In[34]:


def json_extract(json_data,i,col1,col2):
    parsed1 = json_data['countries'][0]['cities'][0]['places'][i][col1]
    parsed2 = json_data['countries'][0]['cities'][0]['places'][i][col2]
    return parsed1,parsed2    


# In[35]:


def unpacking_bike_numbers(column):
    """ 
    getting unique list of bikes
    """
    bike_unpack = pd.DataFrame(df[column].tolist(), index=df.index)
    colnames = list(bike_unpack.columns.values)
    all_bikes = []
    all_bikes = bike_unpack[0]
    
    for c in colnames:
        data= bike_unpack[c]
        pd.concat([all_bikes,data])
    all_bikes = all_bikes.unique()
    return all_bikes


# In[36]:


bike_lst = []
df_files = pd.DataFrame(filenames(r'C:\Users\steff\Documents\DataScience Bootcamp\Bike\json\\'),
                   columns=('file','day','time'))
day = df_files.groupby(by=('day')).size()
day.reset_index()


# In[17]:


singleday = df_files[(df_files['day'] == '20190327') ]
singleday = singleday.values.tolist()


# In[38]:


for f in singleday:
    json_data = parse_json(f)
    for i in range(0,3000):
        try: 
            avail_bikes = json_data['countries'][0]['cities'][0]['available_bikes']
            num_places = json_data['countries'][0]['cities'][0]['num_places']
            refresh_rate = json_data['countries'][0]['cities'][0]['refresh_rate']
            uid, name = json_extract(json_data,i,'uid','name')
            lat, lng = json_extract(json_data,i,'lat','lng')
            bikes, booked_bikes = json_extract(json_data,i,'bikes','booked_bikes')
            free_racks, bike_racks = json_extract(json_data,i,'free_racks','bike_racks') 
            terminal_type, spot = json_extract(json_data,i,'terminal_type','spot') 
            if spot==True:
                spot='station'
            else:
                spot='floating'           
            bike_numbers, number = json_extract(json_data,i,'bike_numbers','number') 

            bike_data = (datetime.strptime((f[1] +' '+ f[2]), "%Y%m%d %H%M%S"),
                         refresh_rate,num_places,avail_bikes,uid,lat,lng,name,
                         number,bikes,booked_bikes,free_racks,bike_racks,terminal_type,
                         spot,bike_numbers)
            bike_lst.append(bike_data)
        except:
            continue


# In[ ]:


#len(bike_lst)


# In[19]:


colnames =('date_time','refresh_rate','num_places','total_avail_bikes','uid','from_lat',
           'from_long','from_station','from_station_id','bikes','booked_bikes','free_racks',
           'bike_racks','terminal_type','from_station_mode','bike_numbers')
df = pd.DataFrame(bike_lst, columns =colnames)
df.tail()


# In[20]:


all_bikes = unpacking_bike_numbers('bike_numbers')
#all_bikes = all_bikes[0:100] # testing
#all_bikes


# In[21]:


def trips_by_bike(df):
    """ generating state for each bike""" 
    pd.options.mode.chained_assignment = None  # default='warn'
    appended_data = []
    for b in all_bikes:
        data = df[df["bike_numbers"].apply(lambda x: True if b in x else False)]
        data.groupby(['from_station']).size()
        data['bike_id'] = b
        # min and max time for this bike on one station
        data['dt_end'] = data.groupby('from_station')['date_time'].transform('max')
        data['dt_start'] = data.groupby('from_station')['date_time'].transform('min')
        data= data[['bike_id','from_station','from_lat','from_long','from_station_id',
                    'from_station_mode','dt_start','dt_end']].copy()
        appended_data.append(data)
    return appended_data


# In[22]:


def generating_duration(df):
    df = df.sort_values(['bike_id','dt_start'], ascending=True)
    df['bike_next_row'] = df['bike_id'].shift(-1)
    df['dt_min_next_row'] = df['dt_start'].shift(-1)
    df['station_next_row'] = df['from_station'].shift(-1)
    df['station_id_next_row'] = df['from_station_id'].shift(-1)
    df['trip_duration'] = np.nan
    df['trip_end_time'] = np.nan
    df['trip_end_time'] = df['trip_end_time'].astype('datetime64[ns]')
    df['diff'] = (df['dt_min_next_row']-df['dt_end']).astype('timedelta64[m]')
    return df


# In[23]:


def generating_next_station(df):
    df['station_mode_next_row'] = df['from_station_mode'].shift(-1)
    df['lat_next_row'] = df['from_lat'].shift(-1)
    df['long_next_row'] = df['from_long'].shift(-1)
    df['to_station'] = np.nan
    df['to_station_id'] = np.nan
    df['to_station_mode'] = np.nan
    df['to_lat'] = np.nan
    df['to_long'] = np.nan
    trips = df.drop_duplicates(subset=['bike_id','from_station'], keep='last')
    return trips


# In[24]:


def generating_destination(trips):
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'trip_end_time'] = trips['dt_min_next_row']
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'to_station'] = trips['station_next_row']
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'to_station_id'] = trips['station_id_next_row']
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'to_station_mode'] = trips['station_mode_next_row']
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'to_lat'] = trips['lat_next_row']
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'to_long'] = trips['long_next_row']
    trips.loc[((trips['bike_id'] == trips['bike_next_row'])
              & (trips['dt_min_next_row'] > trips['dt_start'])), 
             'trip_duration'] = trips['diff']
    return trips


# In[25]:


def trip_ids(df, day):
    newindex = np.arange(int(day)*1000, int(day)*1000+len(df.index), 1)
    df['trip_id'] = newindex
    return df


# In[26]:


# generating trips data
appended_data = trips_by_bike(df)
trips = pd.concat(appended_data,ignore_index=True)
trips = generating_duration(trips)
trips = generating_next_station(trips)
trips = generating_destination(trips)

trips = trip_ids(trips, singleday[0][1])


# In[27]:


#trips.head()


# In[28]:


trips.shape


# In[29]:


df_trip = trips[['trip_id','bike_id','trip_duration','dt_end','trip_end_time',
         'from_station','from_station_id','from_station_mode','from_lat','from_long',
         'to_station','to_station_id','to_station_mode','to_lat','to_long'
         ]]
df_trip = df_trip.rename(columns = {'dt_end':'trip_start_time'})


# In[30]:


df_trip.to_csv(r'trips\\trips_2019-03-27.csv')


# In[ ]:





# In[ ]:




