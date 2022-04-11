# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 17:08:03 2022

@author: zhang
"""

import pandas as pd
from math import radians, cos, sin, asin, sqrt
from sklearn.neighbors import KNeighborsClassifier
from math import *
file = pd.read_csv(r'C:\Users\zhang\Desktop\门店地铁分析\上海地铁数据.csv').dropna(axis =1)

metro_info = file[file['Type']== '地铁站'].reset_index()
store_info = file[file['Type']== '门店'].reset_index()

data_fit = metro_info.iloc[:, [6, 7]]
y = [1] * len(data_fit)

find_x = store_info.iloc[:, [6, 7]]


def geodistance(lng1,lat1,lng2,lat2):
  lng1,lat1,lng2,lat2 = map(radians,[float(lng1),float(lat1),float(lng2),float(lat2)])
  dlon = lng2 - lng1
  dlat = lat2 - lat1
  a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  distance=2*asin(sqrt(a))*6371*1000
  distance=round(distance/1000,3)
  return distance


knn = KNeighborsClassifier(n_neighbors=1,
                           algorithm='ball_tree',
                           metric=lambda s1, s2:geodistance(*s1, *s2))
knn.fit(data_fit, y)
distance, points = knn.kneighbors(find_x, n_neighbors=2, return_distance=True)

#print (distance[0:2])
#print(points[:2])
#tmp = metro_info.iloc[points[0]]


s = pd.DataFrame(store_info.iloc[0]).T
tmp = metro_info.iloc[points[0]]
tmp['距离'] = distance[0]
s['距离'] = '被求点0'
s.columns = tmp.columns
tmp = s.append(tmp)

result = pd.DataFrame()
for i, row in store_info.iterrows():
    tmp = metro_info.iloc[points[i]]
    tmp['距离'] = distance[i]
    s = pd.DataFrame(row).T
    s['距离'] = f'被求点{i}'
    s.columns = tmp.columns
    tmp = s.append(tmp)
    result = result.append(tmp)
result


result.to_excel(r'C:\Users\zhang\Desktop\门店地铁分析\上海门店地铁站匹配.xlsx')

  


  



