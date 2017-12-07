"""
This program will plot two maps of airports, for flight delay rates and durations.
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sklearn.preprocessing import MinMaxScaler

data_path = '../2016_data_new/2016_{}_new.csv'
# longitude and latitude of airports
loc = {'ATL':(-84.4,33.6), 'BOS':(-71,42.4), 'BWI':(-76.7,39.2), 'CLT':(-80.9,35.2), 'DCA':(-77,38.5),
       'DEN':(-104.7,39.9), 'DFW':(-97,32.9), 'DTW':(-83.4,42.4), 'EWR':(-74.2, 41.7), 'FLL':(-80.2,26.1),
       'IAH':(-95.3,30), 'JFK':(-73.8,40.6), 'LAS':(-115.2,36.1), 'LAX':(-118.4,33.9), 'LGA':(-73.9,42.8),
       'MCO':(-81.3,28.4), 'MDW':(-87.8,41.5), 'MSP':(-93.2,44.9), 'ORD':(-87.9,42.5), 'PHL':(-75.2,40),
       'PHX':(-112,33.4), 'SAN':(-117.2,32.7), 'SEA':(-122.3,47.5), 'SFO':(-122.4,37.6), 'SLC':(-112,40.8)
      }


def get_data(path):
    """
    concatenate data to a pandas dataframe
    :param path: path where flight delay data is stored
    :return: pandas dataframe
    """
    assert isinstance(path, str)
    dflist = []
    for i in range(1,13):
        fn = path.format(i)
        df = pd.read_csv(fn, index_col=0)
        dflist.append(df)
    df = pd.concat(dflist, ignore_index=True)
    return df


def plot_map(delays):
    """
    plot delay rate or delay duration for each airport
    :param delays: pandas series of delay rates/durations for each airport
    :return: none
    """
    assert isinstance(delays, pd.Series)
    # scale percentage to integers in a range for plotting
    scaler = MinMaxScaler(feature_range=(3, 20))
    pc_tran = scaler.fit_transform(delays.reshape(-1, 1)).astype(int)

    # plot
    plt.figure(figsize=(20, 10))
    m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49, projection='lcc', lat_0=45, lon_0=-100)
    m.drawcoastlines(color='g')
    m.drawcountries(color='g', linewidth=2)
    m.drawstates(color='g')
    for i in range(len(loc)):
        x, y = loc[delays.index[i]]
        x, y = m(x, y)
        plt.plot(x, y, marker='o', markerfacecolor='yellow', markeredgecolor='red', markersize=pc_tran[i])
        plt.text(x, y, delays.index[i])
    plt.show()


def main():
    df = get_data(data_path)

    # select 25 most flown airports
    grouped = df.groupby(['ORIGIN'])
    grp_size = grouped.size().sort_values(ascending=False)
    airports = list(grp_size.index[:25])

    # get count of totals and delays per airport
    selected = df.loc[df['ORIGIN'].isin(airports)]
    total_grp = selected.groupby(['ORIGIN']).size()
    delays = selected.loc[selected['ARR_DELAY']>0]
    delay_grp = delays.groupby(['ORIGIN']).size()

    # get average delay duration per airport
    ap_dl = delays.groupby(['ORIGIN'])['ARR_DELAY'].mean()

    # compute percentage of delays per airport
    ap_pc = delay_grp.divide(total_grp)

    # plot delay rate and delay duration
    plot_map(ap_dl)
    plot_map(ap_pc)


if __name__ == '__main__':
    main()
