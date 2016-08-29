
# coding: utf-8

# ## Cleaning Data from Talking Data Kaggle competition for Dashboard
# 
# This notebook does the necessary data cleaning to output dashboard_data.csv and dashboard_data.json using both the given datasets in the competition and also real-world map data from China.

# In[81]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from shapely.geometry import Point, shape
import json


# In[82]:

a = os.getcwd()

path1 = a + '\data\gender_age_train.csv'
path2 = a + '\data\phone_brand_device_model.csv'
path3 = a + '\data\events.csv'

train = pd.read_csv(path1)
phone_brand = pd.read_csv(path2)
events = pd.read_csv(path3)

with open(a + '\data\china_provinces_en.json') as data_file:
    provinces_json = json.load(data_file)
    
train.head()


# In[83]:

n_samples = 30000
top_10_brands_en = {'华为':'Huawei', '小米':'Xiaomi', '三星':'Samsung', 'vivo':'vivo', 'OPPO':'OPPO', 
                    '魅族':'Meizu', '酷派':'Coolpad', '乐视':'LeEco', '联想':'Lenovo', 'HTC':'HTC'}

df = train.merge(events, how='left', on='device_id').merge(phone_brand, how='left', on='device_id')
df = df[df['longitude'] != 0].sample(n=n_samples)
df['phone_brand_en'] = df['phone_brand'].apply(lambda phone_brand: top_10_brands_en[phone_brand] if (phone_brand in top_10_brands_en) else 'Other')
df.head()


# In[84]:

def get_age_segment(age):
    if age <= 22:
        return '22-'
    elif age <= 26:
        return '23-26'
    elif age <= 28:
        return '27-28'
    elif age <= 32:
        return '29-32'
    elif age <= 38:
        return '33-38'
    else:
        return '39+'

df['age_segment'] = df['age'].apply(lambda age: get_age_segment(age))
df.head()


# In[85]:

def get_location(longitude, latitude, provinces_json):
    point = Point(longitude,latitude)
    
    for record in provinces_json['features']:
        polygon = shape(record['geometry'])
        if polygon.contains(point):
            return record['properties']['name']
    return 'other'


# In[86]:

df['location'] = df.apply(lambda row: get_location(row['longitude'], row['latitude'], provinces_json), axis=1)


# In[87]:

df.to_csv(a + "\\data\\dashboard_data.csv",)


# In[88]:

cols_to_keep = ['timestamp', 'longitude', 'latitude', 'phone_brand_en', 'gender', 'age_segment', 'location']
df_clean = df[cols_to_keep].dropna()
df_clean.head()


# In[89]:

df_clean.to_json(a + "\\data\\dashboard_data.json",orient='records')

