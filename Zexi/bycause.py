# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:35:53 2017

@author: CC-arol
"""
import matplotlib.pyplot as plt
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
subset=["CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY"]

mask = df['ARR_DELAY'] > 14
df_delay = df.loc[mask]
df_delay.loc[mask, 'ARR_DELAY'] = 15
grp = df_delay.groupby('ARR_DELAY')
num_delay = grp.size()

#df_delay_cause = df.dropna(subset=["CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY"])
mask_carrier = df['CARRIER_DELAY'] > 0
df_delay.loc[mask_carrier, 'CARRIER_DELAY'] = 1
df_delay.loc[mask, 'ARR_DELAY'] = 0
grp_carrier = df_delay.groupby('CARRIER_DELAY')
num_carrier = grp_carrier.size()

mask_weather = df['WEATHER_DELAY'] > 0
df_delay.loc[mask_weather, 'WEATHER_DELAY'] = 1
df_delay.loc[mask, 'ARR_DELAY'] = 0
grp_weather = df_delay.groupby('WEATHER_DELAY')
num_weather = grp_weather.size()

mask_nas = df['NAS_DELAY'] > 0
df_delay.loc[mask_nas, 'NAS_DELAY'] = 1
df_delay.loc[mask, 'ARR_DELAY'] = 0
grp_nas = df_delay.groupby('NAS_DELAY')
num_nas = grp_nas.size()

mask_secure = df['SECURITY_DELAY'] > 0
df_delay.loc[mask_secure, 'SECURITY_DELAY'] = 1
df_delay.loc[mask, 'ARR_DELAY'] = 0
grp_secure = df_delay.groupby('SECURITY_DELAY')
num_secure = grp_secure.size()

mask_late = df['LATE_AIRCRAFT_DELAY'] > 0
df_delay.loc[mask_late, 'LATE_AIRCRAFT_DELAY'] = 1
df_delay.loc[mask, 'ARR_DELAY'] = 0
grp_late = df_delay.groupby('LATE_AIRCRAFT_DELAY')
num_late = grp_late.size()


grp_others = df_delay.groupby('ARR_DELAY')
num_others = grp_others.size()

per_carrier = num_carrier.loc[1] * 1.0 / num_delay.loc[15]
per_weather = num_weather.loc[1] * 1.0 / num_delay.loc[15]
per_nas = num_nas.loc[1] * 1.0 / num_delay.loc[15]
per_secure = num_secure.loc[1] * 1.0 / num_delay.loc[15]
per_late = num_late.loc[1] * 1.0 / num_delay.loc[15]
#per_others = num_others.loc[15] * 1.0 / num_delay.loc[15]

labels = 'Carrier', 'NAS', 'Weather', 'Security', 'Late aricraft'
sizes = [per_carrier, per_nas, per_weather, per_secure, per_late]
colors = ['gold',  'lightcoral', 'yellowgreen','black', 'purple']
explode = (0, 0.1, 0, 0, 0)  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()