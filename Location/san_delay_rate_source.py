"""
@author Yuhan Chen
This module contains a SourceData class.
"""

import pandas as pd
import numpy as np


class SourceData(object):
    """
    This class reads source data files of flight delay and extracts various information.
    """

    def __init__(self):
        """
        Get original dataframe of all flight information and another dataframe of flights departing from SAN
        """
        self.df, self.data = self.__read_data()

    def __read_data(self):

        """
        Read data from source data files.
        :return: a dataframe of all flight information and another dataframe of flights departing from SAN
        """
        dflist = []
        for i in range(1, 13):
            fn = '../2016_data_new/2016_{}_new.csv'.format(i)
            df = pd.read_csv(fn, index_col=0)
            dflist.append(df)
        df = pd.concat(dflist, ignore_index=True)

        # select all flights with ORIGIN at SAN
        san = df.loc[df['ORIGIN'] == 'SAN']
        return df, san

    def dest(self):
        """
        selected airports
        :return: a list of selected airports sorted in alphabetical order
        """
        airports = sorted(['ATL', 'ORD', 'DEN', 'LAX', 'DFW', 'SFO', 'PHX', 'LAS', 'IAH', 'SEA',
                    'MSP', 'MCO', 'DTW', 'BOS', 'EWR', 'CLT', 'SLC', 'JFK', 'BWI', 'LGA',
                    'MDW', 'FLL', 'SAN', 'DCA', 'PHL'])
        return airports

    def cities(self):
        """
        get cities for each airport
        :return: a list of cities in the same order and airports
        """
        airports = self.dest()
        cities = []
        for ap in airports:
            origin_df = self.df.loc[self.df['ORIGIN']==ap]
            city = origin_df['ORIGIN_CITY_NAME'].unique()[0]
            cities.append(city)
        return cities

    def carrier(self):
        """
        get airlines that fly from SAN
        :return: a list of airlines leaving from SAN, sorted in alphabetical order
        """
        san = self.data
        airports = self.dest()
        selected = san.loc[san['DEST'].isin(airports)]
        airlines = selected['UNIQUE_CARRIER'].unique()
        return sorted(list(airlines))

    def source_data(self):
        """
        generate delay rate data
        :return: a dictionary of airlines, whose values are dictionaries of months,
        whose values are a tuple of airports and relative sizes for plotting.
        """
        san = self.data
        airports = self.dest()
        selected = san.loc[san['DEST'].isin(airports)]
        airlines = self.carrier()

        # save data in a dict, airport -> month -> (airlines, size)
        delay_ap = {}
        for ap in airports:
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