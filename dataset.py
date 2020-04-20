import pandas as pd
import numpy as np

class Data:
    def __init__(self):
        self.dataframe()
        self.parse_data()
        print("dataset initialized")
    def dataframe(self):
        self.confirmed_df = pd.read_csv("data/time_series_covid19_confirmed_global.csv")
        self.deaths_df = pd.read_csv("data/time_series_covid19_deaths_global.csv")
        self.recovered_df = pd.read_csv("data/time_series_covid19_recovered_global.csv")

        self.confirmed_df.drop("Province/State", axis=1,inplace=True)
        self.deaths_df.drop("Province/State", axis=1, inplace=True)
        self.recovered_df.drop("Province/State", axis=1, inplace=True)

        self.confirmed_df = self.confirmed_df.groupby(self.confirmed_df['Country/Region']).aggregate(np.sum)
        self.deaths_df = self.deaths_df.groupby(self.deaths_df['Country/Region']).aggregate(np.sum)
        self.recovered_df = self.recovered_df.groupby(self.recovered_df['Country/Region']).aggregate(np.sum)
    def parse_data(self):
        # Confirmed data
        self.confirmed_dict = {}
        for row in self.confirmed_df.iterrows():
            country_name_c = row[0]
            country_data_c = row[1][2:].to_numpy()
            self.confirmed_dict[country_name_c] = country_data_c
        # Death data
        self.death_dict = {}
        for row in self.deaths_df.iterrows():
            country_name_d = row[0]
            country_data_d = row[1][2:].to_numpy()
            self.death_dict[country_name_d] = country_data_d
        # Recovery data
        self.recover_dict = {}
        for row in self.recovered_df.iterrows():
            country_name_r = row[0]
            country_data_r = row[1][2:].to_numpy()
            self.recover_dict[country_name_r] = country_data_r
