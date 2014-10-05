import datetime as dt
import QSTK.qstkutil.qsdateutil as date_util
import QSTK.qstkutil.DataAccess as data_access
import QSTK.qstkutil.tsutil as tsu

#######################################################################################################
def portfolio_simulate(start_date, end_date, symbols, allocations):
    """ For the given portfolio and dates, calculate the std deviation of daily returns (volatility), the average
     daily return, the sharpe ratio, and the cumulative return """

    # Generate timestamps for the NYSE closing times
    closing_time = dt.timedelta(hours=16)
    timestamps = date_util.getNYSEdays(start_date, end_date, closing_time)

    # Get adjusted closing prices
    stock_dao = data_access.DataAccess('Yahoo', cachestalltime=0)
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

# vol, daily_ret, sharpe, cum_ret = portfolio_simulate(
#     dt.datetime(2010, 1, 1), dt.datetime(2010, 1, 6),
#     ['BRCM', 'TXN', 'IBM', 'HNZ'], [0.4, 0.3, 0.1, 0.2])

# vol, daily_ret, sharpe, cum_ret = portfolio_simulate(
#     dt.datetime(2010, 1, 1), dt.datetime(2010, 1, 6),
#     ['AXP', 'HPQ', 'IBM', 'HNZ'], [0.0, 0.0, 0.0, 1.0])

start, end, symbols, allocations, sharpe, std_deviation, ave_daily_ret, cum_ret = portfolio_simulate(
    dt.datetime(2011, 1, 1), dt.datetime(2011, 12, 31),
    ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])

print "Start date: ", start
print "End date: ", end
print "Symbols: ", symbols
print "Allocations: ", allocations
print "Sharpe ratio: ", sharpe
print "Volatility (std_dev of daily returns): ", std_deviation
print "Average daily return: ", ave_daily_ret
print "Cumulative return: ", cum_ret

##################################################################################################################
#
# Start Date:  2010-01-01
# End Date:  2010-01-06
# Symbols:  ['BRCM', 'TXN', 'IBM', 'HNZ']
# Optimal Allocations:  [0.4, 0.3, 0.1, 0.2]
# Sharpe Ratio: -15.874507866387544
# Volatility (stdev of daily returns): 0.004585591209447
# Average Daily Return: -0.004585591209447
# Cumulative Return*: 0.990828817581106

# Start Date: January 01, 2010
# End Date: January 06, 2010
# Symbols: ['AXP', 'HPQ', 'IBM', 'HNZ']
# Optimal Allocations: [0.0, 0.0, 0.0, 1.0]
# Sharpe Ratio: -15.8745078664
# Volatility (stdev of daily returns): 0.00255950857435
# Average Daily Return: -0.00255950857435
# Cumulative Return: 0.994880982851
#
# Start Date: January 01, 2011
# End Date: January 06, 2011
# Symbols: ['AAPL', 'GLD', 'GOOG', 'XOM']
# Optimal Allocations: [0.4, 0.4, 0.0, 0.2]
# Sharpe Ratio: -7.20612630186
# Volatility (stdev of daily returns): 0.00348343046782
# Average Daily Return: -0.00158127988131
# Cumulative Return: 0.995245460263
#

#
#
# Start Date: January 01, 2011
# End Date: January 06, 2011
# Symbols: ['ABT', 'ACAS', 'ACE', 'ADI']
# Optimal Allocations: [0.9, 0.0, 0.1, 0.0]
# Sharpe Ratio: 10.5804226507
# Volatility (stdev of daily returns): 0.00410726333041
# Average Daily Return: 0.00273750735072
# Cumulative Return: 1.00820969947
##################################################################################################################

# Example 1
# Start Date: January 1, 2011
# End Date: December 31, 2011
# Symbols: ['AAPL', 'GLD', 'GOOG', 'XOM']
# Optimal Allocations: [0.4, 0.4, 0.0, 0.2]
# Sharpe Ratio: 1.02828403099
# Volatility (stdev of daily returns):  0.0101467067654
# Average Daily Return:  0.000657261102001
# Cumulative Return:  1.16487261965

# Example 2
# Start Date: January 1, 2010
# End Date: December 31, 2010
# Symbols: ['AXP', 'HPQ', 'IBM', 'HNZ']
# Optimal Allocations:  [0.0, 0.0, 0.0, 1.0]
# Sharpe Ratio: 1.29889334008
# Volatility (stdev of daily returns): 0.00924299255937
# Average Daily Return: 0.000756285585593
# Cumulative Return: 1.1960583568


