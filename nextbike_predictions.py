#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


# In[2]:


df = pd.read_pickle('all_trips.pkl')
df.head()


# ### Day of Week

# In[6]:


df['dow'] = df.trip_start_time.dt.day_name()
df['hour'] = df.trip_start_time.dt.hour
sns.set_style("darkgrid")
ax  = sns.FacetGrid(data=df.groupby([
    'dow',
    'hour'
]).hour.count().to_frame(name='day_hour_count').reset_index(), col='dow', col_order=[
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
], col_wrap=4)
ax.map(sns.barplot, 'hour', 'day_hour_count')


# ### Predict

# In[101]:


daily = df.set_index('trip_start_time').groupby(pd.Grouper(freq='D')).size()
daily = pd.DataFrame(daily)
daily = daily.reset_index()
daily.columns = ['ds', 'y']
daily.head()


# In[102]:


m = Prophet()
m.fit(daily)


# In[103]:


future = m.make_future_dataframe(periods=5)
future.tail()


# In[104]:


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
forecast.to_pickle('forecast.pkl')


# In[105]:


fig1 = m.plot(forecast)


# ### Hourly

# In[124]:


hourly = df.set_index('trip_start_time').groupby(pd.Grouper(freq='2h')).size()
hourly = pd.DataFrame(hourly)
hourly = hourly.reset_index()
hourly.columns = ['ds', 'y']
hourly.head()


# In[125]:


mh = Prophet()
mh.fit(hourly)


# In[126]:


futureh = mh.make_future_dataframe(periods=120)
futureh.tail()


# In[127]:


forecasth = mh.predict(future)
forecasth[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[128]:


forecasth.to_pickle('forecast_hourly.pkl')


# In[129]:


figh = mh.plot(forecasth)


# In[ ]:





# In[ ]:




