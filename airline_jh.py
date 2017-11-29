#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:16:49 2017

@author: tangjinhao
"""
import pandas as pd
import numpy as np
l = []
for i in range(1,13):
    f_name = "data/2016_"
    f_name += str(i) + ".csv"
    l.append(pd.read_csv(f_name))
df = pd.concat(l, ignore_index=True)

#reader = pd.read_csv("data/2016_1.csv") 
# set the flight of early arrival to zero

mask = df['ARR_DELAY'] < 0
df.loc[mask, 'ARR_DELAY'] = 0

grp = df.groupby('AIRLINE_ID')
#airline and their flights
airline = grp.size()

delay = grp.aggregate({'ARR_DELAY':np.sum})

#1.  calculate the average delay for each flight
l = dict()
for i in airline.index:
    l[i] = delay.loc[i]['ARR_DELAY'] * 1.0 / airline.loc[i]
    
# calcuate the percentage of each airline:
mask_delay = df['ARR_DELAY'] > 0
df['DELAY_P'] = mask_delay
delay_flight = df.groupby('AIRLINE_ID')['DELAY_P'].sum()
delay_per = dict()
for i in airline.index:
    delay_per[i] = delay_flight[i] *1.0*100/ airline[i]

#2.  calculate the average delay: for each hour of the day

