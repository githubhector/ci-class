import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

import QSTK.qstkutil.qsdateutil as date_util
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as data_access

def create_pdf(t_stamps, data, legend, y_label, x_label, file_name):
    plt.clf()
    plt.plot(t_stamps, data)
    plt.legend(legend)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(file_name, format='pdf')

print "Selecting symbols and time period..."
symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
timestamp_start = dt.datetime(2007, 1, 1)
timestamp_end = dt.datetime(2010, 12, 31)
time_of_day = dt.timedelta(hours=16)
timestamps = date_util.getNYSEdays(timestamp_start, timestamp_end, time_of_day)

print "Reading data from Yahoo..."
stock_dao = data_access.DataAccess('Yahoo')
data_items = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
stock_data = stock_dao.get_data(timestamps, symbols, data_items)
stock_data_dict = dict(zip(data_items, stock_data))

print "Generating adjusted close pdf file..."
adjusted_close_prices = stock_data_dict['close'].values
create_pdf(timestamps, adjusted_close_prices, symbols, "Adjusted close prices", "Date", "adjusted-closed-prices.pdf")

print "Generating normalized adjusted close pdf file..."
normalized_adjusted_close_prices = adjusted_close_prices / adjusted_close_prices[0, :]
create_pdf(timestamps, normalized_adjusted_close_prices, symbols, "Normalized adjusted close", "Date", "normalized-adjusted-close.pdf")

print "Generating normalized daily returns pdf file..."
normalized_daily_returns = normalized_adjusted_close_prices.copy()
tsu.returnize0(normalized_daily_returns)
create_pdf(timestamps, normalized_daily_returns, symbols, "Normalized daily returns", "Date", "normalized-daily-returns.pdf")
