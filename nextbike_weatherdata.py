#!/usr/bin/env python
# coding: utf-8

# In[110]:


from weatherbit.api import Api
import pandas as pd


# In[111]:


api_key = "e8e380da5ad943a5a6d923b573db05f9"
lat = 52.510008
lon = 13.404954

api = Api(api_key)

# Query by lat/lon
forecast = api.get_forecast(lat=lat, lon=lon)
#forecast = api.get_forecast(city="Berlin", state="Berlin", country="DE")
"""
# To get a daily forecast of temperature, and precipitation:
pd.DataFrame(forecast.get_series(['temp']))"""


# In[112]:


from datetime import datetime
from datetime import timedelta

dates = pd.date_range(start='20190311', end='20190328', freq='D')
df_dates =pd.DataFrame(dates, columns=['start'])
df_dates['end'] = df_dates.shift(-1)
dates = df_dates.values


# ### Hourly

# In[113]:


hist_temp = []
for st,en in dates[:-1]:
    start = (st.astype(str)[0:10])
    end = (en.astype(str)[0:10])
    api.set_granularity('hourly')
    data = api.get_history(lat=lat, lon=lon, 
                          start_date=start, end_date=end)
    hist_temp.append(data)


# In[114]:


temp_lst = []
liquid_precip_lst = []
humidity_lst = []
wind_spd_lst = []
for h in hist_temp:
    liquid_precip = h.get_series(['precip'])
    temp = h.get_series(['temp'])
    humidity  = h.get_series(['rh'])
    wind_spd = h.get_series(['wind_spd'])
    temp_lst += temp
    liquid_precip_lst += liquid_precip
    humidity_lst += humidity
    wind_spd_lst += wind_spd


# In[115]:


data.city_name


# In[116]:


pd_t = pd.DataFrame(temp_lst)
pd_l = pd.DataFrame(liquid_precip_lst)
pd_h = pd.DataFrame(humidity_lst)
pd_w = pd.DataFrame(wind_spd_lst)


# In[117]:


df = pd_t.merge(pd_l, on='datetime')
df = df.merge(pd_h, on='datetime')
df = df.merge(pd_w, on='datetime')


# In[118]:


df.to_pickle('weather_hourly.pkl')


# In[119]:


df.head()


# ### Daily

# In[120]:


hist_temp_d = []
for st,en in dates[:-1]:
    start = (st.astype(str)[0:10])
    end = (en.astype(str)[0:10])
    api.set_granularity('daily')
    data = api.get_history(lat=lat, lon=lon, 
                          start_date=start, end_date=end)
    hist_temp_d.append(data)


# In[121]:


temp_lst = []
liquid_precip_lst = []
humidity_lst = []
wind_spd_lst = []
for h in hist_temp_d:
    liquid_precip = h.get_series(['precip'])
    temp = h.get_series(['temp'])
    humidity  = h.get_series(['rh'])
    wind_spd = h.get_series(['wind_spd'])
    temp_lst += temp
    liquid_precip_lst += liquid_precip
    humidity_lst += humidity
    wind_spd_lst += wind_spd


# In[122]:


pd_t = pd.DataFrame(temp_lst)
pd_l = pd.DataFrame(liquid_precip_lst)
pd_h = pd.DataFrame(humidity_lst)
pd_w = pd.DataFrame(wind_spd_lst)


# In[123]:


df_d = pd_t.merge(pd_l, on='datetime')
df_d = df_d.merge(pd_h, on='datetime')
df_d = df_d.merge(pd_w, on='datetime')


# In[124]:


df_d.to_pickle('weather_daily.pkl')


# In[125]:


df_d.head()


# In[ ]:




