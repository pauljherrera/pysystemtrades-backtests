
import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt

from private.estimatedsystemavanti import futures_system
from sysdata.configdata import Config
from sysdata.csvdata import csvFuturesData

pandl_df = pd.DataFrame()
# Initializing system.
my_config = Config("private.nocarryconfig2.yaml")
data = csvFuturesData("private.noCarryData")
#This is the path to the CSV data.
system = futures_system(log_level="on", config=my_config, data=data)
# Making the backtest for the complete portfolio.
instruments = system.config.instruments


portfolio = system.accounts.portfolio()

info = {}

for item in instruments:
    series = []
    series.append(data.get_raw_price(item))
    series.append(system.accounts.get_buffered_position(item))
    series.append(portfolio.to_frame()[item].cumsum())


    df = pd.concat( series, axis = 1)
    df = df.rename(columns = {0 : 'buffered Position',item:'Profit&Loss'})
    info[item] = df
    print(info[item])


#Showing useful plots and stats.

print("\n\nProfits and loss curve for the complete portfolio:")
portfolio.curve().plot()
plt.title("Profits and loss curve for the complete portfolio:")
plt.show()
                                                 
print("\n\nCompounded profits and loss curve for the complete portfolio:")
portfolio.cumulative().curve().plot()
plt.title("Compounded profits and loss curve for the complete portfolio:")
plt.show()


print("\n\nProfits and loss curve for each one of the assets:")
portfolio.to_frame().cumsum().plot()
plt.title("Profits and loss curve for each one of the assets:")
plt.show()

print("\n\nDrawdown chart:")
portfolio.drawdown().plot()

plt.title("Drawdown chart:")
plt.show()

print("\n\nBacktest stats:")
pprint(system.accounts.portfolio().stats())

