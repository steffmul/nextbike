#!/usr/bin/env python
# coding: utf-8

import time
import json
import requests


for n in range(0, 60):
    time.sleep(300)
    url = 'https://api.nextbike.net/maps/nextbike-live.json?city=362'
    response = requests.get(url).json()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'json/response'+timestr+'.json'
    with open(filename, 'w') as outfile:
        json.dump(response, outfile)
