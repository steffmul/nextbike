#!/usr/bin/env python
# coding: utf-8


import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


df = pd.read_pickle('all_trips.pkl')
df.shape


# Trip duration
sns.set()
x = df['trip_duration']
ax = sns.distplot(x.to_list())


sns.set()
x_detail = df[
    'trip_duration'][df['trip_duration'].between(1, 60, inclusive=True)]
ax = sns.distplot(x_detail.to_list())


# trips per day & hour
timeseries = df.set_index('trip_start_time')
x = timeseries.resample('H').size()
sns.lineplot(x=x.index, y=x.values)
sns.set_style("darkgrid")


timeseries = df.set_index('trip_start_time')
x = timeseries.resample('d').size()

ax = sns.barplot(x=x.index.strftime('%m-%d'), y=x.values)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
sns.set_style("darkgrid")


# Weather
# hourly
temp_per_hour = pd.read_pickle('weather_hourly.pkl')
temp_per_hour[['datetime', 'temp']].head(2)
trips_per_hour = df.groupby([pd.Grouper(key='trip_start_time', freq='H')]
                            ).size().reset_index(name='trips')
trips_per_hour.head(2)
trips_per_hour = trips_per_hour.join(
    temp_per_hour.set_index('datetime'),
    on='trip_start_time')
trips_per_hour.head(2)

timeseries = trips_per_hour.set_index('trip_start_time')
x1 = timeseries['trips']
x2 = timeseries['temp']
sns.lineplot(x=x1.index, y=x1.values, color="g", label='trips per hour')
ax2 = plt.twinx()
sns.lineplot(x=x1.index, y=x2.values, color="b", ax=ax2, label='temp')
ax2.legend
plt.legend(loc='upper left', labels=['temperature'])
sns.set_style("darkgrid")
timeseries['temp'].corr(timeseries['trips'])


# daily
temp_per_day = pd.read_pickle('weather_daily.pkl')
trips_per_day = df.groupby(
    [pd.Grouper(key='trip_start_time', freq='d')]).size().reset_index(
        name='trips')
trips_per_day = trips_per_day.join(
    temp_per_hour.set_index('datetime'),
    on='trip_start_time')
trips_per_day = trips_per_day.set_index('trip_start_time')
d1 = trips_per_day['trips']
d2 = trips_per_day['temp']
sns.lineplot(x=d1.index, y=d1.values, color="g", label='trips per day')
ax2 = plt.twinx()
sns.lineplot(x=d1.index, y=d2.values, color="b", ax=ax2, label='temp')
ax2.legend
plt.legend(loc='upper left', labels=['temperature'])
sns.set_style("darkgrid")
trips_per_day['temp'].corr(trips_per_day['trips'])


# most frequent trips
grouped = df.groupby(
                    ['from_station', 'from_lat', 'from_long',
                    'from_station_mode', 'to_station', 'to_lat', 'to_long',
                    'to_station_mode']
                    ).size()
grouped.shape
grouped = pd.DataFrame(grouped).reset_index()
grouped.columns = ['from_station', 'from_lat', 'from_long',
                    'from_station_mode', 'to_station', 'to_lat', 'to_long',
                    'to_station_mode', 'cnt']
grouped = grouped.sort_values(by='cnt', ascending=False)
grouped.to_pickle('station_combis.pkl')

# top 10 pick up & return stations
df.groupby(['from_station']).size().sort_values(ascending=False).head(10)
df.groupby(['to_station']).size().sort_values(ascending=False).head(10)

sns.barplot(x="total", y="abbrev", data=crashes,
            label="Total", color="b")


df.groupby('from_station_mode')['from_station'].nunique()
