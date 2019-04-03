#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


df = pd.read_pickle('all_trips.pkl')
df.head()


# Day of Week
df['dow'] = df.trip_start_time.dt.day_name()
df['hour'] = df.trip_start_time.dt.hour
sns.set_style("darkgrid")
ax = sns.FacetGrid(data=df.groupby(
    ['dow', 'hour']
    ).hour.count().to_frame(
        name='day_hour_count').reset_index(), col='dow', col_order=[
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'],
    col_wrap=4)
ax.map(sns.barplot, 'hour', 'day_hour_count')


# Predict
daily = df.set_index('trip_start_time').groupby(pd.Grouper(freq='D')).size()
daily = pd.DataFrame(daily)
daily = daily.reset_index()
daily.columns = ['ds', 'y']
daily.head()

m = Prophet()
m.fit(daily)

future = m.make_future_dataframe(periods=5)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
forecast.to_pickle('forecast.pkl')


fig1 = m.plot(forecast)


# Hourly
hourly = df.set_index('trip_start_time').groupby(pd.Grouper(freq='2h')).size()
hourly = pd.DataFrame(hourly)
hourly = hourly.reset_index()
hourly.columns = ['ds', 'y']
hourly.head()


mh = Prophet()
mh.fit(hourly)
futureh = mh.make_future_dataframe(periods=120)
futureh.tail()

forecasth = mh.predict(future)
forecasth[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


forecasth.to_pickle('forecast_hourly.pkl')

figh = mh.plot(forecasth)
