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
print "normalized values:\n", normalized_values

# Calculate the portfolio statistics
total_return = normalized_values[normalized_values.index[-1]]
print "Total return: ", total_return

daily_returns = tsu.returnize0(normalized_values)
print "Daily returns: ", daily_returns

ave_daily_return = daily_returns.mean()
print "Avg daily return: ", ave_daily_return

std_deviation = daily_returns.std()
print "Std deviation:", std_deviation

sharpe_ratio = tsu.get_sharpe_ratio(daily_returns, 0.0)[0]
print "Sharp ratio:", sharpe_ratio


def portfolio_simulate(start_date, end_date, symbols, allocations):
    """ For the given portfolio and dates, calculate the std deviation of daily returns (volatility), the average
     daily return, the sharpe ratio, and the cumulative return """

    # Generate timestamps for the NYSE closing times
    closing_time = dt.timedelta(hours=16)
    timestamps = date_util.getNYSEdays(start_date, end_date, closing_time)

    # Get adjusted closing prices
    #stock_dao = data_access.DataAccess('Yahoo', cachestalltime=0)
    stock_dao = data_access.DataAccess('Yahoo')
    stock_data_as_list_of_data_frames = stock_dao.get_data(timestamps, symbols, ['close'])
    portfolio_closing_values = stock_data_as_list_of_data_frames[0]

    # Calculate adjusted closing prices normalized relative to initial closing prices
    initial_portfolio_closing_values = portfolio_closing_values.values[0,:]
    portfolio_normalized_closing_values = portfolio_closing_values / initial_portfolio_closing_values

    # Calculated portfolio normalized values
    portfolio_normalized_weighted_closing_values = portfolio_normalized_closing_values * allocations
    portfolio_normalized_values = portfolio_normalized_weighted_closing_values.sum(axis=1)

    # Calculate the portfolio statistics
    cumulative_return = portfolio_normalized_values[-1]
    daily_returns = tsu.returnize0(portfolio_normalized_values)
    ave_daily_return = daily_returns.mean()
    std_deviation = daily_returns.std()
    sharpe_ratio = tsu.get_sharpe_ratio(daily_returns, 0.0)[0]

    return start_date, end_date, symbols, allocations, sharpe_ratio, std_deviation, ave_daily_return, cumulative_return





