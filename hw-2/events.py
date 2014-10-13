import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as date_util
import datetime as datetime
import QSTK.qstkutil.DataAccess as data_access
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as event_profiler

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(symbols, data_dictionary):
    actual_close_dataframe = data_dictionary['actual_close']
    market_series = actual_close_dataframe['SPY']

    # Creating an empty dataframe. We copy it from actual_close_dataframe just to get the right dataframe size.
    events_data_frame = copy.deepcopy(actual_close_dataframe)
    events_data_frame = events_data_frame * np.NAN

    # Time stamps for the event range
    timestamps = actual_close_dataframe.index

    for symbol in symbols:
        print "Working on symbol: ", symbol
        for i in range(1, len(timestamps)):
            # Get the symbol prices for yesterday and today
            symprice_today = actual_close_dataframe[symbol].ix[timestamps[i]]
            symprice_yesterday = actual_close_dataframe[symbol].ix[timestamps[i - 1]]

            # Event is found if the symbol drops from >= 8 to < 8
            if symprice_yesterday >= 7.0 and symprice_today < 7.0:
                events_data_frame[symbol].ix[timestamps[i]] = 1
                print "Event occurred for symbol %s: timestamp: %s: yesterday: %s, today: %s"\
                      % (symbol, timestamps[i], symprice_yesterday, symprice_today)

    return events_data_frame


if __name__ == '__main__':

    print "Starting..."

    start = datetime.datetime(2008, 1, 1)
    end = datetime.datetime(2009, 12, 31)
    ldt_timestamps = date_util.getNYSEdays(start, end, datetime.timedelta(hours=16))


    #symbol_list = "sp5002008" # S&P 500 for 2008
    symbol_list = "sp5002012"  # S&P 500 for 2012

    print "Getting data for symbol list: ", symbol_list

    dataobj = data_access.DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list(symbol_list)
    symbols.append('SPY')

    data_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    data_as_list_of_dataframes = dataobj.get_data(ldt_timestamps, symbols, data_keys)

    data_dictionary = dict(zip(data_keys, data_as_list_of_dataframes))

    for s_key in data_keys:
        data_dictionary[s_key] = data_dictionary[s_key].fillna(method='ffill')
        data_dictionary[s_key] = data_dictionary[s_key].fillna(method='bfill')
        data_dictionary[s_key] = data_dictionary[s_key].fillna(1.0)

    print "Finding events..."

    events = find_events(symbols, data_dictionary)

    print "Creating study..."
    event_profiler.eventprofiler(events, data_dictionary, i_lookback=20, i_lookforward=20,
                                 s_filename="seven_dollar_event-" + symbol_list + ".pdf", b_market_neutral=True,
                                 b_errorbars=True,
                                 s_market_sym='SPY')


