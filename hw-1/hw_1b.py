import datetime as dt
import QSTK.qstkutil.qsdateutil as date_util
import QSTK.qstkutil.DataAccess as data_access
import QSTK.qstkutil.tsutil as tsu

#######################################################################################################
def portfolio_simulate(start_date, end_date, symbols, allocations):
    """ For the given portfolio and dates, calculate the std deviation of daily returns (volatility), the average
     daily return, the sharpe ratio, and the cumulative return """
    print "start_date: ", start_date.strftime("%m/%d/%Y")
    print "end_date: ", end_date.strftime("%m/%d/%Y")
    print "symbols: ", symbols
    print "allocations: ", allocations

    # Generate timestamps for the NYSE closing times
    closing_time = dt.timedelta(hours=16)
    timestamps = date_util.getNYSEdays(start_date, end_date, closing_time)

    # Get data from yahoo for the given symbols
    print "Reading data from Yahoo..."
    stock_dao = data_access.DataAccess('Yahoo', cachestalltime=0)

    print "\n\nPortfolio historical closing prices as list of data frames:"
    stock_data_as_list_of_data_frames = stock_dao.get_data(timestamps, symbols, ['close'])
    print stock_data_as_list_of_data_frames

    print "\n\nPortfolio historical closing prices as a data frame:"
    portfolio_closing_data_as_data_frame = stock_data_as_list_of_data_frames[0]
    print portfolio_closing_data_as_data_frame

    print "\n\nPortfolio historical closing prices as a data dictionary:"
    stock_data_dict = dict(zip(['close'], stock_data_as_list_of_data_frames))
    print stock_data_dict

    print "\n\nPortfolio historical closing prices:"
    print stock_data_dict['close']

    print "Initial portfolio closing values:"
    initial_portfolio_closing_values = portfolio_closing_data_as_data_frame.values[0,:]
    print initial_portfolio_closing_values

    print "Portfolio data frame normalized relative to initial closing values:"
    normalized = portfolio_closing_data_as_data_frame / initial_portfolio_closing_values
    print normalized

    print "Normalized data multiplied by allocations"
    normalized_mult_by_allocations = normalized * allocations
    print normalized_mult_by_allocations

    print "Portfolio values as a series: "
    port_values = normalized_mult_by_allocations.sum(axis=1)
    print port_values

    print "Portfolio cumulative return: "
    last_element = port_values[-1]
    print "last element: ", last_element
    cumulative_return = last_element
    print "cumulative_return:"
    print cumulative_return


    print "Daily returns for the portfolio"
    daily_returns = tsu.returnize0(port_values)
    print daily_returns

    print "Average daily return:"
    ave_daily_return = daily_returns.mean()
    print ave_daily_return

    print "Standard deviation of daily returns:"
    std_deviation = daily_returns.std()
    print std_deviation

    print "Sharpe ratio:"
    sharpe_ratio = tsu.get_sharpe_ratio(daily_returns, 0.0)
    print sharpe_ratio


    # TODO: readup on pandas: http://pandas.pydata.org
    # TODO: readup on numpy: http://www.numpy.org
    # TODO: check this out: http://ipython.org/notebook.html

    #tsu.returnize0(stock_data_dict)






    print "DONE"
    return 1, 2, 3, 4
    #return std_daily_ret, ave_daily_ret, sharpe_ratio, cummulative_ret
#######################################################################################################




# vol, daily_ret, sharpe, cum_ret = portfolio_simulate(
#     dt.datetime(2010, 1, 1), dt.datetime(2010, 1, 6),
#     ['BRCM', 'TXN', 'IBM', 'HNZ'], [0.4, 0.3, 0.1, 0.2])

# vol, daily_ret, sharpe, cum_ret = portfolio_simulate(
#     dt.datetime(2010, 1, 1), dt.datetime(2010, 1, 6),
#     ['AXP', 'HPQ', 'IBM', 'HNZ'], [0.0, 0.0, 0.0, 1.0])

vol, daily_ret, sharpe, cum_ret = portfolio_simulate(
    dt.datetime(2011, 1, 1), dt.datetime(2011, 12, 31),
    ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])




print "Done..."


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


