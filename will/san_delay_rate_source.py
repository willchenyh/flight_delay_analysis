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
            fn = '../2016_data/2016_{}_new.csv'.format(i)
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
        return sorted(list(airlines))

    def source_data(self):
        san = self.data
        airports = self.dest()
        selected = san.loc[san['DEST'].isin(airports)]
        airlines = self.carrier()
        """
        save data in a dict
        airport -> month -> (airlines, size)
        """
        delay_ap = {}
        for ap in airports:
            #     pc_list = []
            delay_m = {}
            for month in range(1, 13):
                month_total = selected.loc[(selected['MONTH'] == month) & (selected['DEST'] == ap)]
                delays = month_total.loc[month_total['ARR_DELAY'] > 14]

                num_delay = delays.groupby(['UNIQUE_CARRIER']).size()
                num_total = month_total.groupby(['UNIQUE_CARRIER']).size()
                delay_pc = num_delay.divide(num_total)

                al_used = list(delay_pc.index)

                delay_al = np.zeros((len(airlines),))
                size_al = np.zeros((len(airlines),))
                for i, al in enumerate(airlines):
                    if al in al_used:
                        delay_al[i] = delay_pc[al]
                        size_al[i] = 20
                delay_m[month] = (delay_al, size_al)

            delay_ap[ap] = delay_m

        return delay_ap