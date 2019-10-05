import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
from decimal import Decimal
import matplotlib.pyplot as plt
from scipy.stats import norm

def round_decimal(x):
    decimal_value = Decimal(x)
    return decimal_value.quantize(Decimal(10) ** -2)


def get_simulation(ticker, name):
    ticker_l = check_dot(ticker)

    data = pd.DataFrame()
    data[ticker_l] = wb.DataReader(ticker_l, data_source='yahoo', start='2007-1-1')['Adj Close']
    last_close = data[ticker_l][-1]
    log_returns = np.log(1 + data.pct_change())
    log_returns.tail()
    data.plot(figsize=(10, 6));
    log_returns.plot(figsize = (10, 6))
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()
    np.array(drift)
    norm.ppf(0.95)
    x = np.random.rand(10, 2)
    norm.ppf(x)
    Z = norm.ppf(np.random.rand(10,2))
    t_intervals = 365
    iterations = 10
    daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, iterations)))
    S0 = data.iloc[-1]
    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0

    for t in range(1, t_intervals):
        price_list[t] = price_list[t - 1] * daily_returns[t]
    plt.figure(figsize=(10,6))
    plt.style.use('dark_background')
    plt.title("1 Year Monte Carlo Simulation for " + name)
    plt.ylabel("Price (P)")
    plt.xlabel("Time (Days)")
    plt.plot(price_list);
    plt.savefig('tempplot.png')
    plt.show()

    data = {
        "mean_365_day_price": str(round_decimal(price_list.mean())),
        "pct": str(round_decimal((price_list.mean() / last_close) * 100)) + '%',
        "ticker": ticker,
        "name": name,
        "last_close": str(last_close)
    }

    return data



def append_L(ticker):
    return ticker + 'L'

def replace_dot(ticker):
    t = ticker.replace('.', '-')
    t = t + '.'
    return append_L(t)

def check_dot(ticker):
    if '.' in ticker[-1]:
        return append_L(ticker)
    elif '.' in ticker[-2]:
        return replace_dot(ticker)
    else:
        return append_L(ticker + '.')
