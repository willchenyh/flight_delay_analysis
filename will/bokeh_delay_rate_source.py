import pandas as pd
import numpy as np


class SourceData(object):

    def __init__(self):
        self.df, self.data = self.__read_data()

    def __read_data(self):
        """get data"""
        """concatenate data"""
        dflist = []
        for i in range(1, 13):
            fn = '../2016_data_new/2016_{}_new.csv'.format(i)
            df = pd.read_csv(fn, index_col=0)
            dflist.append(df)
        df = pd.concat(dflist, ignore_index=True)

        """select all flights with ORIGIN at SAN"""
        san = df.loc[df['ORIGIN'] == 'SAN']
        return df, san

    def dest(self):
        """select flights going to following airports"""
        airports = sorted(['ATL', 'ORD', 'DEN', 'LAX', 'DFW', 'SFO', 'PHX', 'LAS', 'IAH', 'SEA',
                    'MSP', 'MCO', 'DTW', 'BOS', 'EWR', 'CLT', 'SLC', 'JFK', 'BWI', 'LGA',
                    'MDW', 'FLL', 'SAN', 'DCA', 'PHL'])
        return airports

    def cities(self):
        """give cities for corresponding airports"""
        airports = self.dest()
        cities = []
        for ap in airports:
            origin_df = self.df.loc[self.df['ORIGIN']==ap]
            city = origin_df['ORIGIN_CITY_NAME'].unique()[0]
            cities.append(city)
        return cities

    def carrier(self):
        san = self.data
        airports = self.dest()
        selected = san.loc[san['DEST'].isin(airports)]
        airlines = selected['UNIQUE_CARRIER'].unique()
        return list(airlines)

    def source_data(self):
        san = self.data
        airports = self.dest()
        selected = san.loc[san['DEST'].isin(airports)]
        airlines = self.carrier()
        """
        save data in a dict
        airline -> month -> (airports, size)
        """
        delay_al = {}
        for al in airlines:
            delay_m = {}
            for month in range(1, 13):
                month_total = selected.loc[(selected['MONTH'] == month) & (selected['UNIQUE_CARRIER'] == al)]
                delays = month_total.loc[month_total['ARR_DELAY'] > 14]

                num_delay = delays.groupby(['DEST']).size()
                num_total = month_total.groupby(['DEST']).size()
                delay_pc = num_delay.divide(num_total)

                ap_used = list(delay_pc.index)

                delay_ap = np.zeros((len(airports),))
                size_ap = np.zeros((len(airports),))
                for i, ap in enumerate(airports):
                    if ap in ap_used:
                        delay_ap[i] = delay_pc[ap]
                        size_ap[i] = 20

                delay_m[month] = (delay_ap, size_ap)

            delay_al[al] = delay_m
        return delay_al