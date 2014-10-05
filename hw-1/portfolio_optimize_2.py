import portfolio_sim as simulate
import datetime as dt
import numpy as np
import sys

start = dt.datetime(2010, 1, 1)
end = dt.datetime(2010, 12, 31)
symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']

largest_sharpe = -sys.float_info.max

for a in range(0, 110, 10):
    for b in range(0, 110, 10):
        for c in range(0, 110, 10):
            for d in range(0, 110, 10):
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
# Start Date: January 1, 2010
# End Date: December 31, 2010
# Symbols: ['AXP', 'HPQ', 'IBM', 'HNZ']
# Optimal Allocations:  [0.0, 0.0, 0.0, 1.0]
# Sharpe Ratio: 1.29889334008
# Volatility (stdev of daily returns): 0.00924299255937
# Average Daily Return: 0.000756285585593
# Cumulative Return: 1.1960583568




