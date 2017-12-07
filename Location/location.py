#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:16:49 2017

@author: tangjinhao
The following plots are intended to be generated:

1. Delay Rate vs State: Map 
2. Delay Rate vs Distance: Bar Chart
3. Delay Rate/Delay Duration vs Airport: Map
4. Delay Rate/Delay Duration vs State/Month: Map with Slider
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import plotly as py 
from bokeh.models.widgets import DataTable, TableColumn

from bokeh.io import curdoc, show
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
from san_delay_rate_source import *
from san_delay_duration_source import *


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

def DelayRate_States(df):
	"""
	Usage: Compute delay rates for each state, produces html code for plot
		   and automatically opens in web browswer. 
	Params: pandas dataframe of flight data 
	Return: nothing 
	Output: the plot will be saved in the local directory: /Visuliazation_Plots/Location  
	"""
	# Check that input is pandas dataframe
	assert isinstance(df, pd.DataFrame)
	
	# Compute delay rates 
	flights_per_state = df['ORIGIN_STATE_NM'].value_counts(sort=False).sort_index()
	delays_per_state = df[df['DEP_DELAY']>15]['ORIGIN_STATE_NM'].value_counts(sort=False).sort_index()
	delay_rates = [rate*100 for rate in list(delays_per_state/flights_per_state)]
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

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
	py.offline.plot( fig, filename='../Visuliazation_Plots/Location/FlightDelayRateMap.html' )

def DelayRate_Distance(df):
    '''
    Usage: calculate and plot percentage of delay: for short, middle and long distance   
    Params: pandas dataframe of flight data 
    Return: None
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Location     
    Note: short distance is defined as flight less than 810 miles
          middle distance is defined as flight larger than 810 miles and less than 2160
          long distance is defined as flight larger than 2160 miles and less than 5000
    '''
    assert isinstance(df, pd.DataFrame)
    SHORT_DELAY = 45
    MIDDLE_DELAY = 180
    dis = [0, 810, 2160, 5000]
    distance = pd.cut(df['DISTANCE'], dis)
    mask_lower = df['ARR_DELAY'] > DELAY_THR
    mask_upper = df['ARR_DELAY'] < SHORT_DELAY
    mask_delay = mask_lower[mask_upper]
    group = pd.concat([distance, mask_delay], axis = 1).groupby('DISTANCE')
    dis_delay = group.sum().iloc[:,0]
    dis_flight = group.size()
    short_delay_dis = (100*dis_delay.div(dis_flight)).tolist()
    # middle distance
    mask_lower = df['ARR_DELAY'] > SHORT_DELAY
    mask_upper = df['ARR_DELAY'] < MIDDLE_DELAY
    mask_delay = mask_lower[mask_upper]
    group = pd.concat([distance, mask_delay], axis = 1).groupby('DISTANCE')
    dis_delay = group.sum().iloc[:,0]
    dis_flight = group.size()
    middle_delay_dis = (100*dis_delay.div(dis_flight)).tolist()
    # long distance
    mask_lower = df['ARR_DELAY'] > MIDDLE_DELAY
    mask_delay = mask_lower
    group = pd.concat([distance, mask_delay], axis = 1).groupby('DISTANCE')
    dis_delay = group.sum().iloc[:,0]
    dis_flight = group.size()
    long_delay_dis = (100*dis_delay.div(dis_flight)).tolist()

    fig = plt.figure()
    (s,m,l) = (short_delay_dis, middle_delay_dis, long_delay_dis)
    interval = range(3)
    width = 0.35 
    alpha = 0.6
    plt.xticks(interval, ["short range flight", "middle range flight", "long range flight"])
    plt.bar(interval, np.array(s), width, color='red', alpha = alpha)
    plt.bar(interval, np.array(m), width, color='blue', bottom=np.array(s), alpha = alpha)
    plt.bar(interval, np.array(l), width, color='green', bottom=np.array(m) + np.array(s), alpha = alpha)
    red_patch = mpatches.Patch(color = 'red', label='short delay', alpha= alpha)
    blue_patch = mpatches.Patch(color = 'blue', label='middle delay', alpha= alpha)
    green_patch = mpatches.Patch(color = 'green', label='large delay', alpha= alpha)
    handles = [red_patch, blue_patch, green_patch]
    plt.ylim(0,25)
    plt.ylabel("Delay Percentage")
    plt.legend(handles = handles)
    plt.grid(False)
    fig.savefig("../Visuliazation_Plots/Location/delay_per_vs_range.png", bbox_inches = 'tight',  dpi= 400)  
    plt.show()
    return (short_delay_dis, middle_delay_dis, long_delay_dis)
 
    
def PercentageMean_map(df, savefig):
    '''
    Usage: Calculate and Plot the plot in the form distribution: airline vs delay_duration. The size of the circle
    represents the average delay. The color refers to the percentage of delay. The darker, the higher percentage. 
    Params: (1) pandas dataframe of flight data (2) A boolean input whether to save the picture
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Location     
    Return: None
    '''        
    
    #remove the early flight
    mask = df['ARR_DELAY'] < 0
    df.loc[mask, 'ARR_DELAY'] = 0

    fig = plt.figure(figsize=(20,10))
    grouped = df.groupby(['ORIGIN'])
    grp_size = grouped.size().sort_values(ascending=False)
    airports = list(grp_size.index)
    
    selected = df.loc[df['ORIGIN'].isin(airports)]
    total_grp = selected.groupby(['ORIGIN']).size()
    
    delays = selected.loc[selected['ARR_DELAY']>=15]
    delay_grp = delays.groupby(['ORIGIN']).size()
    
    ap_pc = delay_grp.divide(total_grp)
    ap_avg = df.groupby(['ORIGIN'])['ARR_DELAY'].mean()  

    

    loc = {'ATL':(-84.4,33.6), 'BOS':(-71,42.4), 'BWI':(-76.7,39.2), 'CLT':(-80.9,35.2), 'DCA':(-77,38.5),
           'DEN':(-104.7,39.9), 'DFW':(-97,32.9), 'DTW':(-83.4,42.4), 'FLL':(-80.2,26.1),
           'IAH':(-95.3,30), 'JFK':(-73.8,40.6), 'LAS':(-115.2,36.1), 'LAX':(-118.4,33.9), 'LGA':(-73.9,42.8),
           'MCO':(-81.3,28.4), 'MDW':(-87.8,41.5), 'MSP':(-93.2,44.9), 'ORD':(-87.9,42.5), 'PHL':(-75.2,40),
           'PHX':(-112,33.4), 'SAN':(-117.2,32.7), 'SEA':(-122.3,47.5), 'SFO':(-122.4,37.6), 'SLC':(-112,40.8)
          }    
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_0=45, lon_0=-100)    
    scl = [(204,229,255),(153,204,255),(102,178,255),(51,153,255),(0,128,255)]   
    scl = [(x *1.0/256,y*1.0/256,z*1.0/256) for (x,y,z) in scl]
    ll = list(np.linspace(0.05, 0.35, num=5))
    scl = [[x,y]    for (x,y) in zip(ll,scl)]   
    def findInterval(scl, p):
        for i in range(len(scl) - 1):
            if p > scl[i][0] and p < scl[i + 1][0]:
                return scl[i][1]
    
    m.drawcoastlines(color='black')
    m.drawcountries(color='black',linewidth=2)
    m.drawstates(color='black')    
    for i in loc:
        x,y = loc[i]
        x, y = m(x, y)
        color = findInterval(scl, ap_pc[i])
        #(ap_avg[i]*15)**2
        plt.plot(x, y, marker='o', markerfacecolor=color, markeredgecolor=color, markersize= ap_avg[i])
        plt.text(x, y, i)
    if savefig:
        fig.savefig("../Visuliazation_Plots/Location/year_map.png", bbox_inches = 'tight',  dpi= 400)      
    plt.show()

    return fig
    
def PercentageMean_MonthInteractionMap():
    '''
    Usage: Plot the percentage mean map with the slider, which can change month from 1 to 12. 
    Params: pandas dataframe of flight data 
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Location     
    Return: None
    '''        
    url = "./month1_map.png"
    bosch_logo = url
    logo_src = ColumnDataSource(dict(url = [bosch_logo]))
    
    page_logo = figure(plot_width = 1000, plot_height = 1000, title="")
    page_logo.toolbar.logo = None
    page_logo.toolbar_location = None
    page_logo.x_range=Range1d(start=0, end=1)
    page_logo.y_range=Range1d(start=0, end=1)
    page_logo.xaxis.visible = False
    page_logo.yaxis.visible = False
    page_logo.xgrid.grid_line_color = None
    page_logo.ygrid.grid_line_color = None
    
    page_logo.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=logo_src)    
    page_logo.outline_line_alpha = 0 
    callback = CustomJS(args=dict(source=logo_src), code="""
        var data = source.data;
        var A = amp.value;
        url = data['url']
        A = Math.round(A)
        for (i = 0; i < url.length; i++) {
            url[i] = "./month" + A.toString() + "_map.png" 
        }
        source.change.emit();
    """)
    #
    amp_slider = Slider(start=1, end=12, value=1, step=1,
                        title="Month", callback=callback)
    callback.args["amp"] = amp_slider
    
    layout = row(
        page_logo,
        widgetbox(amp_slider),
    )
    output_file("../Visuliazation_Plots/Location/map_over_month_interact.html", title="slider.py example")
    curdoc().add_root(page_logo)
    show(layout)
    
def PercentageMean_MonthMap(df):
    '''
    Usage: Plot the percentage mean map of the year.
    Params: pandas dataframe of flight data 
    Output: the plot will be saved in the local directory: /Visuliazation_Plots/Location     
    Return: None
    '''        
    assert isinstance(df, pd.DataFrame)    
    for num in range(1,13):
        df_month = df.groupby('MONTH').get_group(num)
        fig = PercentageMean_map(df_month, False)
        fig.savefig("../Visuliazation_Plots/Location/month" + str(num) + "_map.png", bbox_inches = 'tight',  dpi= 400)


def main():
    #concatenate data into single pandas dataframe
    df = concat_data()
    # Compute relevant features and generate plots
    DelayRate_States(df)
    DelayRate_Distance(df)
    PercentageMean_map(df, True)
    PercentageMean_MonthMap(df)
    PercentageMean_MonthInteractionMap()


if __name__ == '__main__':
	main()
