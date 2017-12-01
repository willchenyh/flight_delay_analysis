#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author Sam Vineyard 

The following plots are intended to be generated:

1. Delay Rate vs Day of Week: Histogram
2. Delay Rate vs Day of Year: Stem Plot
3. Delay Rate vs State: Colorbar and US Map
"""

import pandas as pd
import numpy as np


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
	Usage: Compute delay rates for each day of week. 
	Param: pandas dataframe of flight data 
	Return: list of delay rates(floats), list of days of week (strings)
	"""
	flights_per_day = df['DAY_OF_WEEK'].value_counts(sort=False)
	delays_per_day = df[df['DEP_DELAY']>15]['DAY_OF_WEEK'].value_counts(sort=False)
	delay_rates = list(delays_per_day/flights_per_day)
	days_of_week = ['MON','TUE','WED','THUR','FRI','SAT','SUN']
	return days_of_week, delay_rates

def DelayRate_DayofYear(df):
	"""
	Usage: Compute delay rates for each day of year.
	Param: pandas dataframe of flight data 
	Return: list of delay rates (floats), list of days of year (integers)
	"""
	flights_per_day = df['FL_DATE'].value_counts(sort=False).sort_index()
	delays_per_day = df[df['DEP_DELAY']>15]['FL_DATE'].value_counts(sort=False).sort_index()
	delay_rates = list(delays_per_day/flights_per_day)
	days_of_year = range(1,366)
	return days_of_year, delay_rates

def DelayRate_States(df):
	"""
	Usage: Compute delay rates for each state.
	Param: pandas dataframe of flight data 
	Return: Delay rates for states in alphabetical order 
	"""
	flights_per_state = df['ORIGIN_STATE_NM'].value_counts(sort=False).sort_index()
	delays_per_state = df[df['DEP_DELAY']>15]['ORIGIN_STATE_NM'].value_counts(sort=False).sort_index()
	delay_rates = list(delays_per_state/flights_per_state)
	return delay_rates 

def main():
	df = concat_data()
	# days_of_week, delay_rates = DelayRate_DayofWeek(df)
	# days_of_year, delay_rates = DelayRate_DayofYear(df)
	print DelayRate_States(df)

if __name__ == '__main__':
	main()
