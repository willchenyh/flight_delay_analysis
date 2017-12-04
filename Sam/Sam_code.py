#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author Sam Vineyard 

The following plots are intended to be generated:

1. Delay Rate vs Day of Week: Bar Chart 
2. Delay Rate vs Day of Year: Stem Plot
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
	Usage: Plot delay rates vs day of week as bar chart 
	Param: pandas dataframe of flight data 
	Return: nothing 
	"""

	# Compute delay rates 
	flights_per_day = df['DAY_OF_WEEK'].value_counts(sort=False)
	delays_per_day = df[df['DEP_DELAY']>15]['DAY_OF_WEEK'].value_counts(sort=False)
	delay_rates = list(delays_per_day/flights_per_day)
	days_of_week = ['NA','MON','TUE','WED','THUR','FRI','SAT','SUN']

	# Plot bar chart 
	fig,ax = plt.subplots()
	num_bars = range(1,len(delay_rates)+1)
	ax.bar(num_bars,delay_rates)
	ax.set_xticklabels(days_of_week)
	ax.set_title('US Flight Delay Rates vs Day of Week in 2016')
	ax.set_xlabel('Delay Rates')
	ax.set_ylabel('Day of Week')
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
	delay_rates = list(delays_per_day/flights_per_day)

	# Plot bar chart 
	fig,ax = plt.subplots()

	# Create range of dates for 2016 year 
	dates = [day for day in date_range(date(2016,1,1),date(2016,12,31),\
			timedelta(days=1))] 

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
	ax.bar(dates,delay_rates)
	plt.gcf().autofmt_xdate()
	ax.set_xlim([date(2016,1,1), date(2016,12,31)])
	ax.set_title('US Flight Delay Rates vs 2016 Year')
	ax.set_xlabel('Date')
	ax.set_ylabel('Delay Rates')
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
	delay_rates = list(delays_per_state/flights_per_state)
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

	# TODO: compute average delay time for each state

	# Plot on US map with colorbar delay rate mapping to each state 
	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
	            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

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
	            title = "Flight Delay Rate")
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
	py.offline.plot( fig, filename='FlightDelayRateMap' )


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
	# DelayRate_DayofYear(df)
	# DelayRate_States(df)

if __name__ == '__main__':
	main()
