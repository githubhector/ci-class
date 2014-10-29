import sys
import csv
import os
import pandas as pd

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

orders_dataframe = pd.read_csv(orders_file)
print "\nOrders data frame:\n", orders_dataframe

# Create date list, without dups
years = [str(x) for x in orders_dataframe['year'].tolist()]
months = [str(x) for x in orders_dataframe['month'].tolist()]
days = [str(x) for x in orders_dataframe['day'].tolist()]

dates = ["%s-%s-%s" % (y, m, d) for y, m, d in zip(years, months, days)]
dates = sorted(list(set(dates))) # Remove dup dates and sort

print "\nUnique order dates:\n", dates

# Create symbol list without dups
symbols = list(set(orders_dataframe['symbol'].tolist()))

# Get the data for these dates and symbols

pass




