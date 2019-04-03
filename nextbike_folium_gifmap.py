#!/usr/bin/env python
# coding: utf-8


import folium, json, requests, glob, os, imageio
from folium import plugins
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
import selenium.webdriver
from datetime import datetime
import cv2
import os


def make_base_map(custom_map):
    custom_map = folium.Map(
        location=[52.510008, 13.404954],
        zoom_start=12)
    return custom_map


def add_flexzone(custom_map):
    path = (r"C:\Users\steff\Documents\DataScience Bootcamp\Bike")
    with open(path+'\geo\flexzone_bn.json') as f:
        bln_zone = json.load(f)
    # add the polgon of the berlin flexzone
    folium.GeoJson(
            bln_zone,
            name='geojson'
            ).add_to(custom_map)
    return custom_map


bikemap = add_flexzone(make_base_map('bikemap'))


df = pd.read_pickle('all_trips.pkl')
df['date_hour'] = df['trip_start_time'].dt.round('h')
date_hour = sorted(df['date_hour'].unique())


path = (r"C:\Users\steff\Documents\DataScience Bootcamp\Bike")
for dh in date_hour:
    dt = pd.to_datetime(dh)
    st_h = (str(dt.date())+'_hh'+str(dt.hour))
    bikemap = add_flexzone(make_base_map('bikemap'))
    for index, row in df.iterrows():
        if dt == row['date_hour']:
                    folium.PolyLine(
                        locations=(
                            [row['from_lat'], row['from_long']],
                            [row['to_lat'], row['to_long']]),
                        opacity=0.5,
                        color='blue',
                        weight=5
                        ).add_to(bikemap)
                    try:
                        bikemap.save(path+f'\maps_html\map{st_h}.html')
                    except:
                        continue


# making an  gif
# get all html files
allFiles = glob.glob(os.path.join(path+"\maps_html\", "*.html"))


# convert html to png
driver = selenium.webdriver.PhantomJS()
for f in allFiles:
    driver.set_window_size(800, 600)  # choose a resolution
    driver.get(r'maps_html/'+f[61:])
    # You may need to add time.sleep(seconds) here
    driver.save_screenshot(f'maps_png/map{f[61:-5]}.png')


png_dir = (r"C:\Users\steff\Documents\DataScience Bootcamp\Bike\maps_png\\")
images = []
for file_name in os.listdir(png_dir):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave("nextbike2.gif", images)


# making a movie
image_folder = (r"C:\Users\steff\Documents\DataScience Bootcamp\Bike\maps_png\\")
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
