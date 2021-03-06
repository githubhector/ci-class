import sys
import csv
import os

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

print "\nReading orders file..."

try:
    orders_file_obj = open(orders_file, 'ru')
    reader = csv.DictReader(orders_file_obj, fieldnames=['year', 'month', 'day', 'symbol', 'action', 'shares'], delimiter=',')
except BaseException as e:
    print "Trouble reading orders file: ", e
    sys.exit(1)

print "Orders:"
for row in reader:
    print row

print "Generating orders dates list..."


print "Generating orders symbols list..."







