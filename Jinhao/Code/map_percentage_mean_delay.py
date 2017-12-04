# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:35:53 2017
@author: CC-arol
"""

import pandas as pd
import numpy as np
DELAY_THR = 15
'''
l = []
for i in range(1,13):
    f_name = "data/2016_"
    f_name += str(i) + ".csv"
    l.append(pd.read_csv(f_name))
df_all = pd.concat(l, ignore_index=True)
'''
df = df_all.groupby('MONTH').get_group(1)

#remove the early flight
mask = df['ARR_DELAY'] < 0
df.loc[mask, 'ARR_DELAY'] = 0

#find the origin 
grouped = df.groupby(['ORIGIN'])
grp_size = grouped.size().sort_values(ascending=False)
airports = list(grp_size.index)
#print airports
# print grp_size

selected = df.loc[df['ORIGIN'].isin(airports)]
# print selected['ORIGIN'].unique()
total_grp = selected.groupby(['ORIGIN']).size()


"""get count of delays per airport"""
delays = selected.loc[selected['ARR_DELAY']>=15]
delay_grp = delays.groupby(['ORIGIN']).size()

# get the mean delay of each airport


"""compute percentage of delays per airport"""
ap_pc = delay_grp.divide(total_grp)
ap_avg = df.groupby(['ORIGIN'])['ARR_DELAY'].mean()
# print ap_pc['ATL'], type(ap_pc['ATL'])
# print ap_pc[0], ap_pc.index[0]
#print ap_pc


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# longitude and latitude of airports
loc = {'ATL':(-84.4,33.6), 'BOS':(-71,42.4), 'BWI':(-76.7,39.2), 'CLT':(-80.9,35.2), 'DCA':(-77,38.9),
       'DEN':(-104.7,39.9), 'DFW':(-97,32.9), 'DTW':(-83.4,42.4), 'EWR':(-74.2, 40.7), 'FLL':(-80.2,26.1),
       'IAH':(-95.3,30), 'JFK':(-73.8,40.6), 'LAS':(-115.2,36.1), 'LAX':(-118.4,33.9), 'LGA':(-73.9,40.8),
       'MCO':(-81.3,28.4), 'MDW':(-87.8,41.8), 'MSP':(-93.2,44.9), 'ORD':(-87.9,42), 'PHL':(-75.2,40),
       'PHX':(-112,33.4), 'SAN':(-117.2,32.7), 'SEA':(-122.3,47.5), 'SFO':(-122.4,37.6), 'SLC':(-112,40.8)
      }

# scale percentage to integers in a range for plotting
from sklearn.preprocessing import MinMaxScaler
#scaler = MinMaxScaler(feature_range=(3,20))
# print ap_pc
#pc_tran = scaler.fit_transform(ap_pc.reshape(-1,1)).astype(int)
# print pc_tran
# non linear

fig = plt.figure(figsize=(20,10))
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_0=45, lon_0=-100)

scl = [(242,240,247),(218,218,235),(188,189,220),(158,154,200),(117,107,177),(84,39,143)]
scl = [(x *1.0/256,y*1.0/256,z*1.0/256) for (x,y,z) in scl]
ll = list(np.linspace(0.05, 0.35, num=6))
scl = [[x,y]    for (x,y) in zip(ll,scl)]

def findInterval(scl, p):
    for i in range(len(scl) - 1):
        if p > scl[i][0] and p < scl[i + 1][0]:
            return scl[i][1]


#find which color it belongs to: 
m.drawcoastlines(color='g')
m.drawcountries(color='g',linewidth=2)
m.drawstates(color='g')
for i in loc:
    x,y = loc[i]
    x, y = m(x, y)
    color = findInterval(scl, ap_pc[i])
    #(ap_avg[i]*15)**2
    plt.plot(x, y, marker='o', markerfacecolor=color, markeredgecolor=color, markersize= ap_avg[i])
    plt.text(x, y, i)
fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month1_map.png", bbox_inches = 'tight',  dpi= 400)
plt.show()