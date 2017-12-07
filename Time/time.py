#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:16:49 2017

@author: tangjinhao
The following plots are intended to be generated:

1. Delay Rate vs Day of Week: Overlapping Bar Chart 
2. Delay Rate vs Day of Year: Bar Chart
3. Delay Rate vs Month of Year: Bar Chart
4. Delay Rate vs Hour of Day: Bar Chart
5. Delay Rate vs Causes: Pie Chart
6. Delay Duration vs Month of Year: Bar Chart with Causes
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import rgb2hex, Normalize
from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.io import curdoc, show
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
from datetime import date, datetime, timedelta
import matplotlib.dates as mdates 


DELAY_THR = 15

def concat_data():
    """
	Usage: Concatenate all csv's (one for each month)
	Return: pandas dataframe 
	Note: CSVs must be in one directory up in "2016_data_new", this function
		  is designed to be run as part of this script within github project 
		  directories. 
    """
    dflist = []
    for i in range(1,13):
        fn = '../2016_data_new/2016_{}_new.csv'.format(i)
        df = pd.read_csv(fn, index_col=0)
        dflist.append(df)
    df = pd.concat(dflist, ignore_index=True)
    df = df.dropna(subset=['DEP_TIME','DEP_DELAY','ARR_TIME','ARR_DELAY'])
    mask = df['ARR_DELAY'] < 0
    df.loc[mask, 'ARR_DELAY'] = 0
    return df 

def DelayRate_DayofYear(df):
	"""
	Usage: Plot two bar charts: delay rates and num of flights  
	Param: pandas dataframe of flight data 
	Return: nothing 
	Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time  
	"""
	# Check that input is pandas dataframe
	assert isinstance(df, pd.DataFrame)

	# Compute delay rates 
	flights_per_day = df['FL_DATE'].value_counts(sort=False).sort_index()
	delays_per_day = df[df['DEP_DELAY']>15]['FL_DATE'].value_counts(sort=False).sort_index()
	delay_rates = [rate*100 for rate in list(delays_per_day/flights_per_day)]

	# Create range of dates for 2016 year 
	dates = [day for day in date_range(date(2016,1,1),date(2016,12,31),\
			timedelta(days=1))] 

	# Plot bar chart for delay rates 
	fig,ax = plt.subplots()
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
	ax.bar(dates,delay_rates,zorder=3)

	# Plot formatting 
	ax.yaxis.grid(True,zorder=0)
	plt.gcf().autofmt_xdate()
	ax.set_xlim([date(2016,1,1), date(2016,12,31)])
	ax.set_title('US Flight Delay Rates vs Day of 2016')
	ax.set_xlabel('Date')
	ax.set_ylabel('Delay Rates (%)')
	plt.show()

	# Bar chart for number of flights per day 
	fig,ax = plt.subplots()
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
	ax.bar(dates,flights_per_day,zorder=1)

	# Plot formatting 
	ax.yaxis.grid(True,zorder=0)
	plt.gcf().autofmt_xdate()
	ax.set_xlim([date(2016,1,1), date(2016,12,31)])
	ax.set_title('Number of Flights per Day in 2016')
	ax.set_xlabel('Date')
	ax.set_ylabel('NUmber of Flights')
    	fig.savefig("../Visuliazation_Plots/Time/delay_rate_over_year.png", bbox_inches = 'tight',  dpi= 400)
	plt.show()	

def DelayRate_Causes(df):
    """
	Usage: Plot pie chart with causues
	Param: pandas dataframe of flight data 
	Return: nothing 
	Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time  
    """
    assert isinstance(df, pd.DataFrame)
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
    per_carrier = num_carrier.loc[1] * 1.0 / num_delay.loc[15]
    per_weather = num_weather.loc[1] * 1.0 / num_delay.loc[15]
    per_nas = num_nas.loc[1] * 1.0 / num_delay.loc[15]
    per_secure = num_secure.loc[1] * 1.0 / num_delay.loc[15]
    per_late = num_late.loc[1] * 1.0 / num_delay.loc[15]
    #per_others = num_others.loc[15] * 1.0 / num_delay.loc[15]
    
    labels = 'Carrier', 'NAS', 'Weather', 'Security', 'Late aricraft'
    sizes = [per_carrier, per_weather, per_nas, per_secure, per_late]
    colors = ['gold',  'yellowgreen', 'lightcoral','black', 'purple']
    explode = (0.1, 0, 0, 0, 0)  # explode 1st slice
     
    # Plot
    fig = plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
    plt.title("Delay Rate vs Causes")
     
    plt.axis('equal')
    fig.savefig("../Visuliazation_Plots/Time/delay_cause.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()	

def DelayRate_DayofWeek(df):
	"""
	Usage: Plot delay rates vs day of week as overlapping bar chart 
	Param: pandas dataframe of flight data 
	Return: nothing 
	Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time  
	"""

	# Check that input is pandas dataframe
	assert isinstance(df, pd.DataFrame)

	# Compute delays and flights per day
	# Note: flights per day has delays subtracted so that when stacked using m
	# 		matplotlib, an overlapping effect is implemented 
	delays_per_day = df[df['DEP_DELAY']>15]['DAY_OF_WEEK'].value_counts(sort=False)
	flights_per_day = df['DAY_OF_WEEK'].value_counts(sort=False)-delays_per_day
	delay_rates = [rate*100 for rate in list(delays_per_day/flights_per_day)]
	days_of_week = ['NA','MON','TUE','WED','THUR','FRI','SAT','SUN']

	# Plot bar chart 
	fig,ax = plt.subplots()
	num_bars = range(1,8)
	delays = ax.bar(num_bars, list(delays_per_day), color='blue',alpha=0.6)
	flights = ax.bar(num_bars, list(flights_per_day), color='blue', bottom=delays_per_day)

	# Add delay rate labels above bars
	for delay,flight,delay_rate in zip(delays,flights,delay_rates):
		height = flight.get_height() + delay.get_height()
		ax.text(flight.get_x() + flight.get_width()/2., 1.02*height,
		        str(round(delay_rate,1))+'%',
		        ha='center', va='bottom')

	# Plot formatting 
	y_limits = ax.get_ylim()
	ax.set_ylim([y_limits[0],1.05*y_limits[1]])
	ax.set_xticklabels(days_of_week)
	ax.set_title('US Flight Delay Rates vs Day of Week in 2016')
	ax.set_xlabel('Day of Week')
	ax.set_ylabel('Number of Flights')
	ax.legend((delays,flights),('Delayed Flights','Total Flights'))
    	fig.savefig("../Visuliazation_Plots/Time/delay_rate_over_weeek.png", bbox_inches = 'tight',  dpi= 400)
	plt.show()
    
def DelayRate_DayofHour(df):
    '''
    Usage: Plot the delay rate vs hour using bar chart
    Param: pandas dataframe of flight data 
    Return: None
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time      
    '''
    interval = []
    for i in range(25):
        interval.append(i*100)
    it = pd.cut(df['DEP_TIME'], interval)
    mask_delay = df['ARR_DELAY'] > DELAY_THR
    group = pd.concat([it, mask_delay], axis = 1).groupby('DEP_TIME')
    it_delay = group.sum().iloc[:,0]
    it_flight = group.size()
    delay_hour = 100*it_delay.div(it_flight)
    fig = plt.figure()
    d = dict()
    colord = {}
    for i in range(len(delay_hour.index)):
        d[delay_hour.index[i]] = str(i)
        colord[delay_hour.index[i]] = 'r'
    delay_hour.rename(d, inplace = True)
    x = [s+":00" for s in delay_hour.index.tolist()]
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
            
    plt.ylim(0,80)
    alpha = 0.6
    red_patch = mpatches.Patch(color = 'red', label='high delay risk', alpha= alpha)
    blue_pathch = mpatches.Patch(color = 'blue', label='middle delay risk', alpha= alpha)
    green_patch = mpatches.Patch(color = 'green', label='low delay risk', )
    handles = [red_patch, blue_pathch, green_patch]
    plt.legend(handles= handles)
    plt.bar(y_pos, y, color = colors,alpha= alpha)
    plt.xticks(y_pos, x, rotation = "vertical")
    plt.ylabel("Delay Percentage")
    plt.xlabel('Hour of day')
    plt.grid(False)
    fig.savefig("../Visuliazation_Plots/Time/delay_rate_over_hour.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()
    
#DelayRate_MonthofYear
def DelayRate_MonthofYear(df):
    '''
    Usage: Plot the delay rate vs momth using bar chart
    Param: pandas dataframe of flight data 
    Return: None
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time      
    '''
    fig = plt.figure()
    mask = df['ARR_DELAY'] < 15
    df.loc[mask, 'ARR_DELAY'] = 0
    df.loc[mask, 'CARRIER_DELAY'] = 0
    df.loc[mask, 'WEATHER_DELAY'] = 0
    df.loc[mask, 'NAS_DELAY'] = 0
    df.loc[mask, 'SECURITY_DELAY'] = 0
    df.loc[mask, 'LATE_AIRCRAFT_DELAY'] = 0
    
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
    fig.savefig("../Visuliazation_Plots/Time/delay_rate_over_month.png", bbox_inches = 'tight',  dpi= 400)    
    plt.show()  
    
def compute_delay_cause_time(df):
    '''
    Usage: Calculate the delay time for each cause
    Param: pandas dataframe of flight data 
    Return: Delay time for each cause
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time      
    '''
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

 
def DelayDuration_Month(df):  
    '''
    Usage: plot the delay duration vs month with causes: using bar chart
    Param: pandas dataframe of flight data 
    Return: None
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Time      
    '''
    fig = plt.figure()
    grp_delay = df.groupby('MONTH')
    
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
    fig.savefig("../Visuliazation_Plots/Time/delay_duration_over_month.png", bbox_inches = 'tight',  dpi= 400)  
    plt.show()
    
def date_range(start, end, delta):
	"""
	Usage: generator that returns range of dates
	Param: start date, end date, time between each date generation
	Return: range of dates 	
	"""

	# Check that inputs are correct type
	assert isinstance(start,date)
	assert isinstance(end,date)
	assert isinstance(delta,timedelta)

	cur = start
	while cur <= end:
	    yield cur
	    cur += delta

def main():
	#concatenate data into single pandas dataframe 
	df = concat_data()
	DelayRate_DayofWeek(df)
	DelayRate_DayofYear(df)
	DelayRate_DayofHour(df)
	DelayRate_MonthofYear(df)
	DelayRate_Causes(df)    
	DelayDuration_Month(df)        
    
    
       
if __name__ == '__main__':
	main()
