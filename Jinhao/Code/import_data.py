#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:16:49 2017

@author: tangjinhao
The following plots are intended to be generated:

1. Delay Rate vs Day of Week: Overlapping Bar Chart 
2. Delay Rate vs Day of Year: Bar Chart
3. Number of Flights vs Day of Year: Bar Chart 
4. Delay Rate vs State: Colorbar and US Map
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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
        fn = '../../2016_data_new/2016_{}_new.csv'.format(i)
        df = pd.read_csv(fn, index_col=0)
        dflist.append(df)
    df = pd.concat(dflist, ignore_index=True)
    df = df.dropna(subset=['DEP_TIME','DEP_DELAY','ARR_TIME','ARR_DELAY'])
    mask = df['ARR_DELAY'] < 0
    df.loc[mask, 'ARR_DELAY'] = 0
    return df 


def per_delay_hour(df):
    '''
    Usage: calculate the average delay for each hour of the day
    Return: None
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
    fig.savefig("../delay_vs_hours.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()
    return delay_hour

def per_delay_distance(df):
    '''
    Usage: calculate and plot percentage of delay: for short, middle and long distance   
    Return: None
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
    fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/delay_per_vs_range.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()
    return (short_delay_dis, middle_delay_dis, long_delay_dis)

def airline_delay_density(df):
    '''
    Usage: calculate and plot the plot in the form distribution: airline vs delay_duration
    Return: None
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
    fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/delay_dis_vs_airline.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()   
    
def percentage_mean_map(df, savefig):
    '''
    Usage: calculate and plot the plot in the form distribution: airline vs delay_duration. The size of the circle
    represents the average delay. The color refers to the percentage of delay. The darker, the higher percentage. 
    Return: None
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(savefig, bool)
    mask = df['ARR_DELAY'] < 0
    df.loc[mask, 'ARR_DELAY'] = 0    
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
           'DEN':(-104.7,39.9), 'DFW':(-97,32.9), 'DTW':(-83.4,42.4), 'EWR':(-74.2, 41.7), 'FLL':(-80.2,26.1),
           'IAH':(-95.3,30), 'JFK':(-73.8,40.6), 'LAS':(-115.2,36.1), 'LAX':(-118.4,33.9), 'LGA':(-73.9,42.8),
           'MCO':(-81.3,28.4), 'MDW':(-87.8,41.5), 'MSP':(-93.2,44.9), 'ORD':(-87.9,42.5), 'PHL':(-75.2,40),
           'PHX':(-112,33.4), 'SAN':(-117.2,32.7), 'SEA':(-122.3,47.5), 'SFO':(-122.4,37.6), 'SLC':(-112,40.8)
          }    
    fig = plt.figure(figsize=(20,10))
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
    fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/year_map.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()
    return fig
    
def map_over_month_interact():
    '''
    Usage: plot the percentage mean map with the slider, which can change month from 1 to 12. 
    Return: None
    '''        
    url = "/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month1_map.png"
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
            url[i] = "/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month" + A.toString() + "_map.png" 
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
    
    output_file("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/map_over_month_interact.html", title="slider.py example")
    curdoc().add_root(page_logo)
    show(layout)
    
def generate_map_over_month(df):
    assert isinstance(df, pd.DataFrame)    
    for num in range(1,13):
        df_month = df.groupby('MONTH').get_group(num)
        fig = percentage_mean_map(df_month, False)
        fig.savefig("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month" + str(num) + "_map.png", bbox_inches = 'tight',  dpi= 400)

def delay_over_month(df):
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
    fig.savefig("Image/bycause.png", bbox_inches = 'tight',  dpi= 400)
    plt.show()
    
def delay_cause_over_month(df):
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
    plt.show()  
    
def compute_delay_cause_time(df):
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

 
def delay_duration_causes_over_month(df):    
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
    plt.show()

def delay_distribution(df):
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
    plt.savefig('delay_duration.png',transparent=True, bboxZ_inches = 'tight')
    plt.show()

def main():
	# concatenate data into single pandas dataframe 
	df = concat_data()
	# Compute relevant features and generate plots 
	#per_delay_hour(df)
	#per_delay_distance(df)
	#airline_delay_density(df)
	#percentage_mean_map(df,True)
	#map_over_month_interact()
	#generate_map_over_month(df)
	#delay_over_month(df)
	#delay_cause_over_month(df)
	#delay_duration_causes_over_month(df)
	delay_distribution(df)
       
if __name__ == '__main__':
	main()
