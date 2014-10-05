import portfolio_sim as simulate
import datetime as dt
import numpy as np
import sys

start = dt.datetime(2011, 1, 1)
end = dt.datetime(2011, 12, 31)
symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']

largest_sharpe = -sys.float_info.max

for a in range(0, 110, 10):
    for b in range(0, 100, 10):
        for c in range(0, 100, 10):
            for d in range(0, 100, 10):
                if (a + b + c + d != 100):
                    continue;
                allocation = [a/100., b/100., c/100., d/100.]
                _, _, _, allocations, sharpe, std_deviation, ave_daily_ret, cum_ret = simulate.portfolio_simulate(
                    start, end, symbols, allocation)
                if sharpe > largest_sharpe:
                    largest_sharpe = sharpe
                    best = {"allocations":allocations,
                            "sharpe": sharpe, "std_deviation": std_deviation, "ave_daily_ret":ave_daily_ret, "cum_ret":cum_ret}


print "\n\n***Best portfolio:"
print "Start date: ", start.strftime("%B %d, %Y")
print "End date: ", end.strftime("%B %d, %Y")
print "Symbols: ", symbols
print "Optimal allocations: ", best["allocations"]
print "Sharpe ratio: ", best["sharpe"]
print "Volatility (std_dev of daily returns): ", best["std_deviation"]
print "Average daily return: ", best["ave_daily_ret"]
print "Cumulative return: ", best["cum_ret"]

# Expected results:
# Start Date: January 1, 2011
# End Date: December 31, 2011
# Symbols: ['AAPL', 'GLD', 'GOOG', 'XOM']
# Optimal Allocations: [0.4, 0.4, 0.0, 0.2]
# Sharpe Ratio: 1.02828403099
# Volatility (stdev of daily returns):  0.0101467067654
# Average Daily Return:  0.000657261102001
# Cumulative Return:  1.16487261965




