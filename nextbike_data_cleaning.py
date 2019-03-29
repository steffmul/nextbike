#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns


# In[2]:


path = (r"C:\Users\steff\Documents\DataScience Bootcamp\Bike\trips")
allFiles = glob.glob(os.path.join(path,"*.csv"))


# In[3]:


np_array_list = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    np_array_list.append(df.values)

comb_np_array = np.vstack(np_array_list)
all_trips = pd.DataFrame(comb_np_array)

all_trips.columns = ['index','trip_id','bike_id','trip_duration','trip_start_time','trip_end_time',
         'from_station','from_station_id','from_station_mode','from_lat','from_long',
         'to_station','to_station_id','to_station_mode','to_lat','to_long' ]


# In[4]:


# remove NaN and negative trip size
all_trips = all_trips.dropna(subset=['trip_duration'])
all_trips['trip_start_time'] = pd.to_datetime(all_trips['trip_start_time'])
all_trips['trip_end_time'] = pd.to_datetime(all_trips['trip_end_time'])


# In[5]:


all_trips = all_trips[all_trips['trip_duration'].between(1, 1440, inclusive=True)]
df['trip_id'] = np.arange(10000, 10000+len(df.index), 1)
all_trips.to_pickle('all_trips.pkl')
all_trips.shape


# In[6]:


all_trips.head()


# In[7]:


all_trips.groupby([all_trips['trip_end_time'].dt.date])['trip_id'].size()


# In[ ]:




