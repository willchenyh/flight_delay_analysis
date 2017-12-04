#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 19:15:16 2017

@author: tangjinhao
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


airline_map = {19393:"Southwest Airlines",19690:"Hawaiian Airlines", 19790:"Delta Air Lines",
   19805:"American Airlines",19930:"Alaska Airlines", 19977:"United Air Lines",20304:"SkyWest Airlines",
 20366:"ExpressJet Airlines",20409:"JetBlue Airways",20416:"Spirit Air Line",20436:"Frontier Airlines",21171:"Virgin America" }


#1. delay percentage vs hour
delay_hour = per_delay_hour()
fig = plt.figure()
d = dict()
colord = {}
for i in range(len(delay_hour.index)):
    d[delay_hour.index[i]] = str(i)
    colord[delay_hour.index[i]] = 'r'
delay_hour.rename(d, inplace = True)
x = delay_hour.index.tolist()
y_pos = np.arange(len(x))
y = delay_hour.iloc[:].tolist()
colors = []
for delay in y:
    if delay < 20:
        colors.append('green')
    elif delay > 35:
        colors.append('red')
    else:
        colors.append('blue')
        
plt.ylim(0,100)
alpha = 0.6
red_patch = mpatches.Patch(color = 'red', label='high delay risk', alpha= alpha)
blue_pathch = mpatches.Patch(color = 'blue', label='middle delay risk', alpha= alpha)
green_patch = mpatches.Patch(color = 'green', label='low delay risk', )
handles = [red_patch, blue_pathch, green_patch]
plt.legend(handles= handles)
plt.bar(y_pos, y, color = colors,alpha= alpha)
plt.xticks(y_pos, x)
plt.ylabel("Delay Percentage")
plt.xlabel('Time of day')
fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/delay_vs_hours.png", bbox_inches = 'tight',  dpi= 400)
plt.show()

#2. delay density vs airline
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
fig = plt.figure()
sns.set_style("darkgrid")
airline_map = {19393:"Southwest Airlines",19690:"Hawaiian Airlines", 19790:"Delta Air Lines",
   19805:"American Airlines",19930:"Alaska Airlines", 19977:"United Air Lines",20304:"SkyWest Airlines",
 20366:"ExpressJet Airlines",20409:"JetBlue Airways",20416:"Spirit Air Line",20436:"Frontier Airlines",21171:"Virgin America" }
fig = plt.figure()
df_den = df.loc[:100, ['ARR_DELAY', 'AIRLINE_ID']]
df_den.AIRLINE_ID = df_den.AIRLINE_ID.apply(lambda i:airline_map[i])
df_den.rename(columns = {"AIRLINE_ID":"AIRLINE"}, inplace = True)

ax3 = sns.stripplot(x="ARR_DELAY", y ="AIRLINE",linewidth = 0.1, data= df_den, jitter=True)
plt.setp(ax3.get_xticklabels(), fontsize=14)
interval = [ 240*i  for i in range(8)]
ax3.set_xticks(interval)
ax3.set_xticklabels(['{:1.0f}h'.format(*[int(y) for y in divmod(x,60)]) for x in ax3.get_xticks()])
ax3.yaxis.label.set_visible(False)
fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/delay_dis_vs_airline.png", bbox_inches = 'tight',  dpi= 400)
plt.show()


# 3. 
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure()
(s,m,l) = per_delay_distance()
interval = range(3)
width = 0.35 
alpha = 0.6
plt.xticks(interval, ["short range flight", "middle range flight", "long range flight"])
p1 = plt.bar(interval, np.array(s), width, color='red', alpha = alpha)
p2 = plt.bar(interval, np.array(m), width, color='blue', bottom=np.array(s), alpha = alpha)
p3 = plt.bar(interval, np.array(l), width, color='green', bottom=np.array(m) + np.array(s), alpha = alpha)
red_patch = mpatches.Patch(color = 'red', label='short delay', alpha= alpha)
blue_patch = mpatches.Patch(color = 'blue', label='middle delay', alpha= alpha)
green_patch = mpatches.Patch(color = 'green', label='large delay', alpha= alpha)
handles = [red_patch, blue_patch, green_patch]
plt.ylim(0,25)
plt.ylabel("Delay Percentage")
plt.legend(handles = handles)
fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/delay_per_vs_range.png", bbox_inches = 'tight',  dpi= 400)
plt.show()