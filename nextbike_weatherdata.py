#!/usr/bin/env python
# coding: utf-8
from weatherbit.api import Api
import pandas as pd
from datetime import datetime
from datetime import timedelta


api_key = "[FILL IN YOUR KEY]"
lat = 52.510008
lon = 13.404954

api = Api(api_key)

# Query by lat/lon
forecast = api.get_forecast(lat=lat, lon=lon)
# forecast = api.get_forecast(city="Berlin", state="Berlin", country="DE"


dates = pd.date_range(start='20190311', end='20190328', freq='D')
df_dates = pd.DataFrame(dates, columns=['start'])
df_dates['end'] = df_dates.shift(-1)
dates = df_dates.values


# Hourly
hist_temp = []
for st, en in dates[:-1]:
    start = (st.astype(str)[0:10])
    end = (en.astype(str)[0:10])
    api.set_granularity('hourly')
    data = api.get_history(
        lat=lat, lon=lon, start_date=start, end_date=end)
    hist_temp.append(data)


temp_lst = []
liquid_precip_lst = []
humidity_lst = []
wind_spd_lst = []
for h in hist_temp:
    liquid_precip = h.get_series(['precip'])
    temp = h.get_series(['temp'])
    humidity = h.get_series(['rh'])
    wind_spd = h.get_series(['wind_spd'])
    temp_lst += temp
    liquid_precip_lst += liquid_precip
    humidity_lst += humidity
    wind_spd_lst += wind_spd


data.city_name


pd_t = pd.DataFrame(temp_lst)
pd_l = pd.DataFrame(liquid_precip_lst)
pd_h = pd.DataFrame(humidity_lst)
pd_w = pd.DataFrame(wind_spd_lst)


df = pd_t.merge(pd_l, on='datetime')
df = df.merge(pd_h, on='datetime')
df = df.merge(pd_w, on='datetime')


df.to_pickle('weather_hourly.pkl')
df.head()


# Daily
hist_temp_d = []
for st, en in dates[:-1]:
    start = (st.astype(str)[0:10])
    end = (en.astype(str)[0:10])
    api.set_granularity('daily')
    data = api.get_history(
        lat=lat, lon=lon, start_date=start, end_date=end)
    hist_temp_d.append(data)


temp_lst = []
liquid_precip_lst = []
humidity_lst = []
wind_spd_lst = []
for h in hist_temp_d:
    liquid_precip = h.get_series(['precip'])
    temp = h.get_series(['temp'])
    humidity = h.get_series(['rh'])
    wind_spd = h.get_series(['wind_spd'])
    temp_lst += temp
    liquid_precip_lst += liquid_precip
    humidity_lst += humidity
    wind_spd_lst += wind_spd


pd_t = pd.DataFrame(temp_lst)
pd_l = pd.DataFrame(liquid_precip_lst)
pd_h = pd.DataFrame(humidity_lst)
pd_w = pd.DataFrame(wind_spd_lst)


df_d = pd_t.merge(pd_l, on='datetime')
df_d = df_d.merge(pd_h, on='datetime')
df_d = df_d.merge(pd_w, on='datetime')


df_d.to_pickle('weather_daily.pkl')

df_d.head()
