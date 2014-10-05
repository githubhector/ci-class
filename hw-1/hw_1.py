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
    stock_data_as_data_frame = stock_data_as_list_of_data_frames[0]
    print stock_data_as_data_frame

    print "\n\nPortfolio historical closing prices as a data dictionary:"
    stock_data_dict = dict(zip(['close'], stock_data_as_list_of_data_frames))
    print stock_data_dict

    print "\n\nPortfolio historical closing prices:"
    print stock_data_dict['close']


    

    # TODO: find out why the close values above don't match data from yahoo website

    # TODO: readup on pandas: http://pandas.pydata.org
    # TODO: readup on numpy: http://www.numpy.org
    # TODO: check this out: http://ipython.org/notebook.html

    #tsu.returnize0(stock_data_dict)







    return 1, 2, 3, 4
    #return std_daily_ret, ave_daily_ret, sharpe_ratio, cummulative_ret
#######################################################################################################





start_date = dt.datetime(2011, 1, 1)
end_date = dt.datetime(2011, 12, 31)





vol, daily_ret, sharpe, cum_ret = portfolio_simulate(start_date, end_date, ['GOOG','AAPL','GLD','XOM'], [0.4, 0.4, 0.0, 0.2])

print "Done..."




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


