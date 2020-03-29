import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

confirmed_df = pd.read_csv("data/time_series_covid19_confirmed_global.csv")
deaths_df = pd.read_csv("data/time_series_covid19_deaths_global.csv")
recovered_df = pd.read_csv("data/time_series_covid19_recovered_global.csv")

confirmed_df.drop("Province/State", axis=1,inplace=True)
deaths_df.drop("Province/State", axis=1, inplace=True)
recovered_df.drop("Province/State", axis=1, inplace=True)

# confirmed information stored in a dictionary with key being country name
confirmed_dict = {}
for row in confirmed_df.iterrows():
    country_name_c = row[1]['Country/Region']
    country_data_c = row[1][3:].to_numpy()
    confirmed_dict[country_name_c] = country_data_c

# death information stored in a dictionary with key being country name
death_dict = {}
for row in deaths_df.iterrows():
    country_name_d = row[1]['Country/Region']
    country_data_d = row[1][3:].to_numpy()
    death_dict[country_name_d] = country_data_d

# recovery information stored in a dictionary with key being country name
recover_dict = {}
for row in recovered_df.iterrows():
    country_name_r = row[1]['Country/Region']
    country_data_r = row[1][3:].to_numpy()
    recover_dict[country_name_r] = country_data_r

c = input("Enter a country: ")

# ensures that the country is in the dictionary
try:
    x = range(len(confirmed_dict[c]))
except:
    print("please enter a valid country name")
    exit() # exits the program if the given country is invalid

# only gathers y-data if the country is valid
y_conf = confirmed_dict[c]
y_dead = death_dict[c]
y_rec = recover_dict[c]

# creating the figure and giving it a title
plt.style.use('seaborn')
fig, axs = plt.subplots(3, 1, constrained_layout=True)
fig.canvas.set_window_title("Covid-19 Data")
fig.suptitle("Coronavirus: " + c)
# axs[0] represents confirmed cases
axs[0].plot(x, y_conf, 'o', c='y')
axs[0].set_title('confirmed vs. time')
axs[0].set_xlabel("days since 1/22/2020")
axs[0].set_ylabel("# of confirmed cases")

# axs[1] represents deaths
axs[1].plot(x, y_dead, 'o', c='r')
axs[1].set_title('deaths vs. time')
axs[1].set_xlabel('days since 1/22/2020')
axs[1].set_ylabel('# of deaths')

# axs[2] represents recovery
axs[2].plot(x, y_rec, 'o', c='g')
axs[2].set_title('recovered vs. time')
axs[2].set_xlabel('days since 1/22/2020')
axs[2].set_ylabel('# of recoveries')
plt.show()
