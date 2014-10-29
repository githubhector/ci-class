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
print "\nOrders data frame:"
print orders_dataframe

# Create string lists of years, months, days
years = [str(x) for x in orders_dataframe['year'].tolist()]
months = [str(x) for x in orders_dataframe['month'].tolist()]
days = [str(x) for x in orders_dataframe['day'].tolist()]

# Create date list of form year-mo-day

pass




