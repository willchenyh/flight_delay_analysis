#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:16:49 2017

@author: tangjinhao
"""
import pandas as pd
import numpy as np
DELAY_THR = 15

l = []
for i in range(1,13):
    f_name = "data/2016_"
    f_name += str(i) + ".csv"
    l.append(pd.read_csv(f_name))
df = pd.concat(l, ignore_index=True)

#drop the not used column
df.drop('Unnamed: 22', axis=1, inplace=True)
df = df.dropna(subset=['DEP_TIME','DEP_DELAY','ARR_TIME','ARR_DELAY'])
# set the flight of early arrival to zero
mask = df['ARR_DELAY'] < 0
df.loc[mask, 'ARR_DELAY'] = 0

#group flights according to airline
grp = df.groupby('AIRLINE_ID')
airline = grp.size()

#1.  calculate the average delay for each flight
'''
output: dictionary. key: airline  value: average delay
'''
def average_delay_airline():
    delay = grp.aggregate({'ARR_DELAY':np.sum})
    l = dict()
    for i in airline.index:
        l[i] = delay.loc[i]['ARR_DELAY'] * 1.0 / airline.loc[i]
    return l
    
#2. calcuate the percentage of each airline:
'''
output: dictionary. key: airline  value: percentage of delay
'''
def per_delay_airline():
    mask_delay = df['ARR_DELAY'] > DELAY_THR
    df['DELAY_P'] = mask_delay
    delay_flight = df.groupby('AIRLINE_ID')['DELAY_P'].sum()
    delay_per = dict()
    for i in airline.index:
        delay_per[i] = delay_flight[i] *1.0*100/ airline[i]
    return delay_per

#3.  calculate the percentage of delay: for each hour of the day
'''
output: dictionary. key: airline  value: percentage of delay
'''
def per_delay_hour():
    interval = []
    for i in range(25):
        interval.append(i*100)
    it = pd.cut(df['DEP_TIME'], interval)
    mask_delay = df['ARR_DELAY'] > DELAY_THR
    group = pd.concat([it, mask_delay], axis = 1).groupby('DEP_TIME')
    it_delay = group.sum().iloc[:,0]
    it_flight = group.size()
    delay_hour = 100*it_delay.div(it_flight)
    return delay_hour

#4. calculate percentage of delay: for short and long distance
# find the DISTANCE, max: 4983.0   min: 28    median: 679
# 810  2160   5000
'''
output: dictionary. key: distance  value: percentage of delay
'''
def per_delay_distance():
    dis = [0, 810, 2160, 5000]
    distance = pd.cut(df['DISTANCE'], dis)
    mask_delay = df['ARR_DELAY'] > DELAY_THR
    group = pd.concat([distance, mask_delay], axis = 1).groupby('DISTANCE')
    dis_delay = group.sum().iloc[:,0]
    dis_flight = group.size()
    delay_dis = 100*dis_delay.div(dis_flight)
    return delay_dis
