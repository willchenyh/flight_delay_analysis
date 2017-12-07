#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:16:49 2017

@author: tangjinhao
The following plots are intended to be generated:
1. Delay Duration vs Airline: Density Plot
2. Delay Duration vs Delay Rate: Curve Plot
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



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

def airline_delay_density(df):
    '''
    Usage: calculate and plot the plot in the form distribution: airline vs delay_duration
    Param: pandas dataframe 
    Return: None
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Airline
    '''
    assert isinstance(df, pd.DataFrame)
    fig = plt.figure()
    sns.set_style("darkgrid")
    airline_map = {19393:"Southwest Airlines",19690:"Hawaiian Airlines", 19790:"Delta Air Lines",
       19805:"American Airlines",19930:"Alaska Airlines", 19977:"United Air Lines",20304:"SkyWest Airlines",
     20366:"ExpressJet Airlines",20409:"JetBlue Airways",20416:"Spirit Air Line",20436:"Frontier Airlines",21171:"Virgin America" }
    fig = plt.figure()
    df_den = df.loc[:, ['ARR_DELAY', 'AIRLINE_ID']]
    df_den.AIRLINE_ID = df_den.AIRLINE_ID.apply(lambda i:airline_map[i])
    df_den.rename(columns = {"AIRLINE_ID":"AIRLINE"}, inplace = True)
    
    ax3 = sns.stripplot(x="ARR_DELAY", y ="AIRLINE",linewidth = 0.1, size=1, data= df_den, jitter=True)
    plt.setp(ax3.get_xticklabels(), fontsize=14)
    plt.xlabel("Delay Duration")
    interval = [ 240*i  for i in range(8)]
    ax3.set_xticks(interval)
    ax3.set_xticklabels(['{:1.0f}h'.format(*[int(y) for y in divmod(x,60)]) for x in ax3.get_xticks()])
    ax3.yaxis.label.set_visible(False)
    fig.savefig("../Visuliazation_Plots/Airline/airline_delay_density.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()   

def delay_distribution(df):
    '''
    Usage: calculate and plot the plot in the form distribution: airline vs delay_duration
    Param: pandas dataframe 
    Return: None
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Airline
    '''
    mask = df['ARR_DELAY'] < 0
    df.loc[mask, 'ARR_DELAY'] = 0
    interval = []
    for i in range(20):
        interval.append(i*15)
    delay_duration = pd.cut(df['ARR_DELAY'], interval)
    delay_duration_percentage = pd.concat([delay_duration], axis = 1).groupby('ARR_DELAY').size() / 5538145 * 100
    fig = delay_duration_percentage.plot(figsize=(10,5))
    plt.xlabel('Delay Time / min') 
    plt.ylabel('Percentage of flights delayed / %')
    plt.title('Duration of delays')
    plt.savefig('../Visuliazation_Plots/Airline/delay_duration.png',transparent=True, bboxZ_inches = 'tight')
    plt.show()

def main():
	#concatenate data into single pandas dataframe 
	df = concat_data()
	airline_delay_density(df)
	delay_distribution(df)
       
if __name__ == '__main__':
	main()
