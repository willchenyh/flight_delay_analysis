# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:18:43 2017

@author: CC-arol
"""
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab 
import pandas as pd
import numpy as np
l = []
for i in range(1,13):
    f_name = "2016_"
    f_name += str(i) + ".csv"
    l.append(pd.read_csv(f_name))
df = pd.concat(l, ignore_index=True)

#drop the not used column
df.drop('Unnamed: 22', axis=1, inplace=True)
df = df.dropna(subset=['DEP_TIME','DEP_DELAY','ARR_TIME','ARR_DELAY'])
# set the flight of early arrival to zero

mask = df['ARR_DELAY'] < 15
df.loc[mask, 'ARR_DELAY'] = 0
mask1 = df['ARR_DELAY'] > 14


grp = df.groupby('MONTH')

df_delay = df.loc[mask1]
grp_delay = df_delay.groupby('MONTH')
#airline and their flights

month_flight = grp.size()
month_delay = grp_delay.size()

#1.  calculate the average delay for each flight
delay_month = dict()
for i in month_flight.index:
    delay_month[i] = month_delay.loc[i] * 100.0 / month_flight.loc[i]

x = pd.Series(delay_month.values(),delay_month.keys())
    
frequency = []
for i in month_flight.index:
    for j in xrange(month_delay.loc[i]):
        frequency.append(i) 

ax1 = x.plot(kind = "bar")
ax1.set_ylim(0,100)
ax1.legend(" ",loc = 'upper center', title = "Delay Rate vs Month")
plt.show() 
