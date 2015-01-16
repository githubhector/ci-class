import datetime as dt
import QSTK.qstkutil.qsdateutil as date_util
import QSTK.qstkutil.DataAccess as data_access
import QSTK.qstkutil.tsutil as tsu
import sys
import pandas as pd

usage = "Usage: analyze.py <values.csv> <benchmark-symbol>"

print "num args: ", len(sys.argv)
print "argv: ", str(sys.argv)

if len(sys.argv) != 3:
    print "Wrong number of parameters:", usage
    exit(1)

values_file = sys.argv[1]
benchmark_sym = sys.argv[2]

print "values_file:", values_file, "\nbenchmark:", benchmark_sym

# Read values file and normalize
values_df = pd.read_csv(values_file)
print "Values data frame:\n", values_df

start_value = values_df.iloc[0,1]
print "starting value:", start_value

normalized_values = values_df['value'] / start_value
#print "normalized values:\n", normalized_values

# Calculate the portfolio statistics
total_return = normalized_values[normalized_values.index[-1]]
print "Total return: ", total_return

daily_returns = tsu.returnize0(normalized_values)
#print "Daily returns: ", daily_returns

ave_daily_return = daily_returns.mean()
print "Avg daily return: ", ave_daily_return

std_deviation = daily_returns.std()
print "Std deviation:", std_deviation

sharpe_ratio = tsu.get_sharpe_ratio(daily_returns, 0.0)[0]
print "Sharp ratio:", sharpe_ratio





