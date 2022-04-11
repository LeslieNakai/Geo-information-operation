# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:41:21 2022

@author: zhang
"""



from urllib.parse import quote
from urllib import request
import json
import xlwt
import json
import pandas as pd
import requests
import os

key = '3ad6db43fd2b7c796d670c756d369eed'
url = 'https://restapi.amap.com/v3/place/text?'

types = '地铁站'
citys = ['北京','上海']
def get_mall(types,city,page):
    params = {
        'key':key,
        'keywords':'',
        'types':types,
        'city':city,
        'children': 1,
        'offset':20,
        'page':page,
        'extensions':'all',        
        }  
    r = requests.get(url,params=params)    
    data = r.json()      
    pois = data['pois']
    file_name = '北上广深地铁数据.csv'
    for poi in pois:
        if len(poi['parent'])==0:
            df = pd.DataFrame({
                '_city' : poi['cityname'],
                '_id' : poi['id'],
                '_name' : poi['name'],
                '_adname' : poi['adname'],
                '_location' : poi['location']
            },index=[0])
        else:
            continue
        if os.path.exists(file_name):
            df.to_csv(file_name, mode='a', header=False,
              index=None, encoding='utf_8_sig')
        else:
            df.to_csv(file_name, index=None, encoding='utf_8_sig')

    return pois 
  
for city in citys:
    page = 1
    while True:
        pois = get_mall(types,city,page)
        if pois == []:
            break
        page+=1
        print(f'\r正在爬取{city}的第{page}页地铁数据',end='')