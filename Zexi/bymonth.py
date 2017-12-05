# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:18:43 2017

@author: CC-arol
"""
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab 
import matplotlib.patches as mpatches
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
df.loc[mask, 'CARRIER_DELAY'] = 0
df.loc[mask, 'WEATHER_DELAY'] = 0
df.loc[mask, 'NAS_DELAY'] = 0
df.loc[mask, 'SECURITY_DELAY'] = 0
df.loc[mask, 'LATE_AIRCRAFT_DELAY'] = 0

mask1 = df['ARR_DELAY'] > 14

test = df.groupby('ARR_DELAY')
test1 = test.size()

grp = df.groupby('MONTH')

df_delay = df.loc[mask1]
grp_delay = df_delay.groupby('MONTH')

#airline and their flights

month_flight = grp.size()
month_delay = grp_delay.size()

#1.  calculate the average delay for each flight
delay_month = dict()
for i in month_flight.index:
    delay_month[i] = month_delay.loc[i] * 1.0 / month_flight.loc[i]

x = pd.Series(delay_month.values(),delay_month.keys())
    

labels = ["Jan","Feb","March","April","May","June","July","Agu","Sept","Oct","Nov","Dec"]
ax1 = x.plot(kind = "bar")
ax1.set_ylim(0,0.3)
ax1.set_xticklabels(labels)
#ax1.legend(" ",loc = 'upper right', title = "Delay Rate vs Month")
plt.title("Delay Rate vs Month")
plt.xlabel("Month")  
plt.ylabel("Delay Rate")
  
plt.show() 
###############################################################################
def compute_delay_cause_time(df):
    #df = grp_delay.get_group(1)

    #mask_delay = df['ARR_DELAY'] > 14
    #delay_time = df.loc[mask_delay1, 'ARR_DELAY']
    #delay_time_sum = delay_time.sum()


    mask_carrier = df['CARRIER_DELAY'] > 0
    carrier_delay_time = df.loc[mask_carrier, 'CARRIER_DELAY']
    carrier_delay_time_sum = carrier_delay_time.sum()
    mask_weather = df['WEATHER_DELAY'] > 0
    weather_delay_time = df.loc[mask_weather, 'WEATHER_DELAY']
    weather_delay_time_sum = weather_delay_time.sum()
    mask_nas = df['NAS_DELAY'] > 0
    nas_delay_time = df.loc[mask_nas, 'NAS_DELAY']
    nas_delay_time_sum = nas_delay_time.sum()
    mask_security = df['SECURITY_DELAY'] > 0
    security_delay_time = df.loc[mask_security, 'SECURITY_DELAY']
    security_delay_time_sum = security_delay_time.sum()
    mask_late = df['LATE_AIRCRAFT_DELAY'] > 0
    late_delay_time = df.loc[mask_late, 'LATE_AIRCRAFT_DELAY']
    late_delay_time_sum = late_delay_time.sum()
    
    return carrier_delay_time_sum, weather_delay_time_sum, nas_delay_time_sum, security_delay_time_sum, late_delay_time_sum
###############################################################################
carrier_delay_time_sum = []
weather_delay_time_sum = []
nas_delay_time_sum = []
security_delay_time_sum = []
late_delay_time_sum = []

bottom_weather = []
bottom_nas = []
bottom_security = []
bottom_late = []
for i in range(12):
    df = grp_delay.get_group(i+1)
    a,b,c,d,e = compute_delay_cause_time(df)
    carrier_delay_time_sum.append(a)
    weather_delay_time_sum.append(b)
    nas_delay_time_sum.append(c)
    security_delay_time_sum.append(d)
    late_delay_time_sum.append(e)
    
    bottom_weather.append(a)
    bottom_nas.append(a+b)
    bottom_security.append(a+b+c)
    bottom_late.append(a+b+c+d)

###############################################################################
fig = plt.figure()
interval = range(12)
width = 0.35 
alpha = 0.8
p1_y = tuple(carrier_delay_time_sum)
p2_y = tuple(weather_delay_time_sum)
p3_y = tuple(nas_delay_time_sum)
p4_y = tuple(security_delay_time_sum)
p5_y = tuple(late_delay_time_sum)
bottom_weather = tuple(bottom_weather)
bottom_nas = tuple(bottom_nas)
bottom_security = tuple(bottom_security)
bottom_late = tuple(bottom_late)
plt.xticks(interval, ["Jan","Feb","March","April","May","June","July","Agu","Sept","Oct","Nov","Dec"])
p1 = plt.bar(interval, np.array(p1_y), width, color='#F14D49', alpha = alpha)
p2 = plt.bar(interval, np.array(p2_y), width, color='#BCA18D', bottom=np.array(bottom_weather), alpha = alpha)
p3 = plt.bar(interval, np.array(p3_y), width, color='#F4ED71', bottom=np.array(bottom_nas), alpha = alpha)
p4 = plt.bar(interval, np.array(p4_y), width, color='#000D29', bottom=np.array(bottom_security), alpha = alpha)
p5 = plt.bar(interval, np.array(p5_y), width, color='#118C8B', bottom=np.array(bottom_late), alpha = alpha)
plt.legend((p1[0], p2[0],p3[0], p4[0],p5[0]), ('Carrier', 'Weather','NAS','Security','Late Aircraft'))
plt.title("Delay Duration with causes vs Month")
plt.xlabel("Month")  
plt.ylabel("Delay Duration with causes(minutes)")
plt.show()



###############################################################################
plt.figure()
x=np.array(df['ARR_DELAY'])
y=np.array(df['CARRIER_DELAY'])
T=np.arctan2(x,y)
plt.scatter(x,y,c=T,s=25,alpha=0.4,marker='o')
#T:散点的颜色
#s：散点的大小
#alpha:是透明程度
fig.savefig("1.png", bbox_inches = 'tight', dpi= 400)
plt.show()
###############################################################################
plt.figure()
x=np.array(df['ARR_DELAY'])
y=np.array(df['WEATHER_DELAY'])
T=np.arctan2(x,y)
plt.scatter(x,y,c=T,s=25,alpha=0.4,marker='o')
#T:散点的颜色
#s：散点的大小
#alpha:是透明程度
fig.savefig("2.png", bbox_inches = 'tight', dpi= 400)
plt.show()
###############################################################################
plt.figure()
x=np.array(df['ARR_DELAY'])
y=np.array(df['NAS_DELAY'])
T=np.arctan2(x,y)
plt.scatter(x,y,c=T,s=25,alpha=0.4,marker='o')
#T:散点的颜色
#s：散点的大小
#alpha:是透明程度
fig.savefig("3.png", bbox_inches = 'tight', dpi= 400)
plt.show()
###############################################################################
plt.figure()
x=np.array(df['ARR_DELAY'])
y=np.array(df['SECURITY_DELAY'])
T=np.arctan2(x,y)
plt.scatter(x,y,c=T,s=25,alpha=0.4,marker='o')
#T:散点的颜色
#s：散点的大小
#alpha:是透明程度
fig.savefig("4.png", bbox_inches = 'tight', dpi= 400)
plt.show()
###############################################################################
plt.figure()
x=np.array(df['ARR_DELAY'])
y=np.array(df['LATE_AIRCRAFT_DELAY'])
T=np.arctan2(x,y)
plt.scatter(x,y,c=T,s=25,alpha=0.4,marker='o')
#T:散点的颜色
#s：散点的大小
#alpha:是透明程度
fig.savefig("5.png", bbox_inches = 'tight', dpi= 400)
plt.show()