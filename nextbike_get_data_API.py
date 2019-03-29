#!/usr/bin/env python
# coding: utf-8

# In[1]:


#basic
import requests, time, os, re, string, wordcloud, spacy
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import json
from bs4 import BeautifulSoup


# In[2]:


for n in range(0,60):
    time.sleep(300)
    url = 'https://api.nextbike.net/maps/nextbike-live.json?city=362'
    response = requests.get(url).json()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'json/response'+timestr+'.json' 
    with open(filename, 'w') as outfile:
        json.dump(response, outfile)


# In[ ]:




