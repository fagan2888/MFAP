"""
Messing around with Yahoo options data. 
WARNING:  WORK IN PROGRESS, NEEDS HELP!!!
Also:  the pandas guide to this is fuzzy, incomplete 

Prepared for the NYU Course "Macroeconomic Foundations for Asset Prices," 
ECO-UB-233.  More at
* https://sites.google.com/site/nyusternmacrofoundations/home
* https://github.com/DaveBackus/MFAP

References 
* http://finance.yahoo.com/q/op?s=SPY+Options
* http://pandas.pydata.org/pandas-docs/stable/remote_data.html#yahoo-finance
* http://pandas.pydata.org/pandas-docs/stable/remote_data.html#yahoo-finance-options

Written by Dave Backus @ NYU, August 2014  
Created with Python 3.4 
"""
import pandas as pd
import pandas.io.data as web
from pandas.io.data import Options
import datetime as dt 

# checking versions 
#print(['Matplotlib version ', plt.__version__])
#print(['Pandas version ', pd.__version__])

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 6, 4.5  # default is 6, 4
mpl.rcParams['legend.fontsize'] = 10  
mpl.rcParams['legend.labelspacing'] = 0.25
mpl.rcParams['legend.handlelength'] = 5

import matplotlib.pylab as plt

#%%

"""
1. Read in Yahoo stock and options prices for SPY (SP 500 "Spyders")  
"""
ticker = 'spy' 

# stock price first (the underlying) 
# pick a recent date and subtract seven days to be sure we get a quote  
# http://pymotw.com/2/datetime/#date-arithmetic
today = dt.date.today()
one_week = dt.timedelta(days=7)
start = today - one_week
stock = web.DataReader(ticker, 'yahoo', start) 
print(stock.tail())        # just to see what we have

# take the last close (that's what the -1 does)
atm = stock.ix[-1,'Close']      # the -1 takes the last observation   

#%%

# get option prices for same ticker 
# http://pandas.pydata.org/pandas-docs/stable/remote_data.html#yahoo-finance-options
option = Options(ticker, 'yahoo')
expiry = dt.date(2014, 12, 20)
data_calls = option.get_call_data(expiry=expiry)
data_puts  = option.get_put_data(expiry=expiry)

print(data_calls.tail()) 
print(data_puts.tail()) 

#%%

# plot puts v strike, call v strike
calls_bid = data_calls['Bid']
calls_ask = data_calls['Ask'] 

calls_strikes = data_calls['Strike']
calls_mid = (data_calls['Bid'] + data_calls['Ask'])/2
puts_strikes = data_puts['Strike']
puts_mid = (data_puts['Bid'] + data_puts['Ask'])/2

plt.plot(calls_strikes, calls_mid, 'r', lw=2, label='calls')
#plt.plot(calls_strikes, calls_ask, 'r', lw=2, label='calls ask')
plt.plot(puts_strikes, puts_mid, 'b', lw=2, label='puts')
plt.axis([120, 250, 0, 50])
plt.axvline(x=atm, color='k', linestyle='--', label='ATM')               
plt.legend(loc='upperleft')

# check put-call parity:  plot bid ask call v call from parity
#%%

"""
2. Implied volatilities 
"""

# BSM formula...

# merge by strike ??