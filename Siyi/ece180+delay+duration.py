
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
DELAY_THR = 15

l = []
for i in range(1,13):
    f_name = "2016_"
    f_name += str(i) + ".csv"
    l.append(pd.read_csv(f_name))
df = pd.concat(l, ignore_index=True)


# In[3]:


#drop the not used column
df.drop('Unnamed: 22', axis=1, inplace=True)
df = df.dropna(subset=['DEP_TIME','DEP_DELAY','ARR_TIME','ARR_DELAY'])


# In[4]:


# set the flight of early arrival to zero
mask = df['ARR_DELAY'] < 0
df.loc[mask, 'ARR_DELAY'] = 0


# In[5]:


interval = []
for i in range(20):
    interval.append(i*15)
delay_duration = pd.cut(df['ARR_DELAY'], interval)


# In[6]:


delay_duration_percentage = pd.concat([delay_duration], axis = 1).groupby('ARR_DELAY').size() / 5538145 * 100  
#delay_duration_percentage = pd.concat([delay_duration_percentage], axis = 1)
#delay_duration_percentage.columns = ["percentage of delay duration"]
#delay_duration_percentage


# In[7]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
delayfig = delay_duration_percentage.plot(figsize=(10,5))
plt.xlabel('Delay Time / min') 
plt.ylabel('Percentage of flights delayed / %')
plt.title('Duration of delays')
plt.savefig('delay_duration.png',transparent=True, bboxZ_inches = 'tight')
plt.show()

