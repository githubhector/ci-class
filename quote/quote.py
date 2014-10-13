import urllib
import urllib2

# See http://www.jarloo.com/yahoo_finance/

symbol = "GOOG,AMZN"
stat_name = "ab" # a = 'ask', b = 'bid'

url = "http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s" % (symbol, stat_name)
request = urllib2.Request(url)
response = urllib2.urlopen(request)
content = response.read().decode().strip()

print symbol, ": ask,bid:\n", content
