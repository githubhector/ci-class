import sys
import os
import pandas as pd
import datetime as dt
import QSTK.qstkutil.qsdateutil as date_util
import QSTK.qstkutil.DataAccess as data_access

usage = "Usage: marketsym.py <starting_cash> <orders_csv_file> <values_csv_output_file>"

print "num args: ", len(sys.argv)
print "argv: ", str(sys.argv)

if len(sys.argv) != 4:
    print "Wrong number of parameters:", usage
    exit(1)

starting_cash = sys.argv[1]
orders_file = sys.argv[2]
values_file = sys.argv[3]

print "Starting cash: ", starting_cash
print "Orders file: ", orders_file
print "Values file: ", values_file

print "Current working directory: ", os.getcwd()

orders_df = pd.read_csv(orders_file)
print "\nOrders data frame:\n", orders_df

# Create sorted list of datetimes, without dups
years = orders_df['year'].tolist()
months = orders_df['month'].tolist()
days = orders_df['day'].tolist()
dates = sorted(list(set([dt.datetime(y, m, d) for y, m, d in zip(years, months, days)])))
print "\nOrder dates in ascending order:\n", dates
start_dt = dates[0]
end_dt = dates[len(dates) - 1]
print "Start:", start_dt, ", end:", end_dt

# Create symbol list without dups
symbols = list(set(orders_df['symbol'].tolist()))
print "\nSymbols:\n", symbols

# Get the data for these dates and symbols
closing_time = dt.timedelta(hours=16)
timestamps = date_util.getNYSEdays(start_dt, end_dt + dt.timedelta(days=1), closing_time)

# Get adjusted closing prices for the symbols on these dates
dao = data_access.DataAccess('Yahoo')
closing_prices = dao.get_data(timestamps, symbols, ['close'])[0]
print "\nAdjusted closing_prices:\n", closing_prices

pass
