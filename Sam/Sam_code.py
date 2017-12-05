#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author Sam Vineyard 

The following plots are intended to be generated:

1. Delay Rate vs Day of Week: Overlapping Bar Chart 
2. Delay Rate vs Day of Year: Bar Chart 
3. Delay Rate vs State: Colorbar and US Map
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
from datetime import date, datetime, timedelta
import plotly as py 



def concat_data():
	"""
	Usage: Concatenate all csv's (one for each month)
	Return: pandas dataframe 
	"""
	dflist = []
	for i in range(1,13):
	    fn = '../2016_data_new/2016_{}_new.csv'.format(i)
	    df = pd.read_csv(fn, index_col=0)
	    dflist.append(df)
	df = pd.concat(dflist, ignore_index=True)
	return df 

def DelayRate_DayofWeek(df):
	"""
	Usage: Plot delay rates vs day of week as overlapping bar chart 
	Param: pandas dataframe of flight data 
	Return: nothing 
	"""

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
	plt.show()

def DelayRate_DayofYear(df):
	"""
	Usage: Plot delay rates vs day of year as bar chart 
	Param: pandas dataframe of flight data 
	Return: nothing 
	"""

	# Compute delay rates 
	flights_per_day = df['FL_DATE'].value_counts(sort=False).sort_index()
	delays_per_day = df[df['DEP_DELAY']>15]['FL_DATE'].value_counts(sort=False).sort_index()
	delay_rates = [rate*100 for rate in list(delays_per_day/flights_per_day)]

	# Create range of dates for 2016 year 
	dates = [day for day in date_range(date(2016,1,1),date(2016,12,31),\
			timedelta(days=1))] 

	# Plot bar chart 
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

def DelayRate_States(df):
	"""
	Usage: Compute delay rates for each state.
	Param: pandas dataframe of flight data 
	Return: Delay rates for states in alphabetical order 
	"""
	
	# Compute delay rates 
	flights_per_state = df['ORIGIN_STATE_NM'].value_counts(sort=False).sort_index()
	delays_per_state = df[df['DEP_DELAY']>15]['ORIGIN_STATE_NM'].value_counts(sort=False).sort_index()
	delay_rates = [rate*100 for rate in list(delays_per_state/flights_per_state)]
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

	# TODO: compute average delay time for each state

	# Plot on US map with colorbar delay rate mapping to each state 
	scl = [[0.0, 'rgb(230,242,255)'],[0.2, 'rgb(179,215,255)'],[0.4, 'rgb(128,187,255)'],\
	            [0.6, 'rgb(77,160,255)'],[0.8, 'rgb(26,133,255)'],[1.0, 'rgb(0,95,204)']]

	data = [ dict(
	        type='choropleth',
	        colorscale = scl,
	        autocolorscale = False,
	        locations = states,
	        z = delay_rates,
	        locationmode = 'USA-states',
	        marker = dict(
	            line = dict (
	                color = 'rgb(0,0,0)',
	                width = 1
	            ) ),
	        colorbar = dict(
	            title = "Flight Delay Rate (%)")
	        ) ]

	layout = dict(
	        title = '2016 Flight Delay Rates vs State',
	        geo = dict(
	            scope='usa',
	            projection=dict( type='albers usa' ),
	            showlakes = True,
	            lakecolor = 'rgb(255, 255, 255)'),
	             )
	    
	fig = dict( data=data, layout=layout )
	py.offline.plot( fig, filename='FlightDelayRateMap.html' )


def date_range(start, end, delta):
	"""
	Usage: generator that returns range of dates
	Param: start date, end date, time between each date generation
	Return: range of dates 	
	"""
	cur = start
	while cur <= end:
	    yield cur
	    cur += delta

def main():
	# concatenate data into single pandas dataframe 
	df = concat_data()

	# Uncomment the plot you want 
	DelayRate_DayofWeek(df)
	DelayRate_DayofYear(df)
	DelayRate_States(df)

if __name__ == '__main__':
	main()
