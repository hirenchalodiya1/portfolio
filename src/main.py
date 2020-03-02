from yahoo import YahooFinanceData
from datetime import datetime
from engine import PyfolioEngine

stock_code = [
    'MSFT',  # Microsoft
    'RS',  # Reliance
    'GOOGL',  # Google
    'AAPL',  # Apple
    'AMZN',  # Amazon
    'TSLA',  # Tesla
    'NFLX',  # netflix
    'FB',  # Facebook
    'GS',  # goldman sachs
    'JPM',  # jp morgan chase
    'MS',  # morgan stanley
    'DIS',  # disney
    'WMT',  # Walmart
    'TXN',  # texas instruments
    'HPE',  # hewlet packard
    'IBM',  # ibm
    'INTC',  # intel
    'NVDA',  # nvidia
    'MA',  # mastercard
    'TCS.NS',
    'SQ',
    'CODX',
    'TDOC',
    'IBIO',
    'PYPL',
]
new_stocks = [
    # 'RELIANCE.NS',
    # 'GC=F',
    # 'ITUB',
    # 'SBIN.NS',
    # 'ICICIBANK.NS',
    # '^NSEBANK',
    # 'BAC',
]
x = set(new_stocks) & set(stock_code)
if x:
    raise ValueError('You have already invested in {}'.format(', '.join(x)))
# Fetch data
data = YahooFinanceData(stock_code, fromdate=datetime(2017, 8, 1), todate=datetime(2020, 2, 1))
data.prepare()

# New stocks data
new_data = YahooFinanceData(new_stocks, fromdate=datetime(2017, 8, 1), todate=datetime(2020, 2, 1))
new_data.prepare()

# Let engine handle rest of it !!
engine = PyfolioEngine(data.data, 0.2, 0.0633, marko={'mu_max': 1.5, 'gp_point': 70}, cap={'compare_point': 0.15},
                       new={'data': new_data.data})
engine.plot(show_marko=True, show_capm=True, show_beta=True)
engine.pprint(show_marko=True, show_capm=True, show_beta=True)
