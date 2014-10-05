import datetime as dt
import QSTK.qstkutil.qsdateutil as date_util
import QSTK.qstkutil.DataAccess as data_access
import QSTK.qstkutil.tsutil as tsu
import unittest as unittest

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


class TestPortSim(unittest.TestCase):
    def test_sim_1(self):
        print "*** TEST 1 ***"
        start, end, symbols, allocations, sharpe, std_deviation, ave_daily_ret, cum_ret = portfolio_simulate(
        dt.datetime(2011, 1, 1), dt.datetime(2011, 12, 31),
        ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])

        print "Start date: ", start.strftime("%B %d, %Y")
        print "End date: ", end.strftime("%B %d, %Y")
        print "Symbols: ", symbols
        print "Allocations: ", allocations
        print "Sharpe ratio: ", sharpe
        print "Volatility (std_dev of daily returns): ", std_deviation
        print "Average daily return: ", ave_daily_ret
        print "Cumulative return: ", cum_ret

        self.assertAlmostEqual(1.02828403099, sharpe, 10)
        self.assertAlmostEqual(0.0101467067654, std_deviation, 10)
        self.assertAlmostEqual(0.000657261102001, ave_daily_ret, 10)
        self.assertAlmostEqual(1.16487261965, cum_ret, 10)

        # Expected results:
        # Start Date: January 1, 2011
        # End Date: December 31, 2011
        # Symbols: ['AAPL', 'GLD', 'GOOG', 'XOM']
        # Optimal Allocations: [0.4, 0.4, 0.0, 0.2]
        # Sharpe Ratio: 1.02828403099
        # Volatility (stdev of daily returns):  0.0101467067654
        # Average Daily Return:  0.000657261102001
        # Cumulative Return:  1.16487261965

    def test_sim_2(self):
        print "*** TEST 2 ***"
        start, end, symbols, allocations, sharpe, std_deviation, ave_daily_ret, cum_ret = portfolio_simulate(
        dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31),
        ['AXP', 'HPQ', 'IBM', 'HNZ'], [0.0, 0.0, 0.0, 1.0])

        print "Start date: ", start.strftime("%B %d, %Y")
        print "End date: ", end.strftime("%B %d, %Y")
        print "Symbols: ", symbols
        print "Allocations: ", allocations
        print "Sharpe ratio: ", sharpe
        print "Volatility (std_dev of daily returns): ", std_deviation
        print "Average daily return: ", ave_daily_ret
        print "Cumulative return: ", cum_ret

        self.assertAlmostEqual(1.29889334008, sharpe, 10)
        self.assertAlmostEqual(0.00924299255937, std_deviation, 10)
        self.assertAlmostEqual(0.000756285585593, ave_daily_ret, 10)
        self.assertAlmostEqual(1.1960583568, cum_ret, 10)

        # Expected results:
        # Start Date: January 1, 2010
        # End Date: December 31, 2010
        # Symbols: ['AXP', 'HPQ', 'IBM', 'HNZ']
        # Optimal Allocations:  [0.0, 0.0, 0.0, 1.0]
        # Sharpe Ratio: 1.29889334008
        # Volatility (stdev of daily returns): 0.00924299255937
        # Average Daily Return: 0.000756285585593
        # Cumulative Return: 1.1960583568

if __name__ == '__main__':
    unittest.main()


