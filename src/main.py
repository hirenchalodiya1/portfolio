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
# Fetch data
data = YahooFinanceData(stock_code, fromdate=datetime(2017, 8, 1), todate=datetime(2020, 2, 1))
data.prepare()

# Let engine handle rest of it !!
engine = PyfolioEngine(data.data, 0.2, 0.0633, marko={'mu_max': 1.5, 'gp_point': 70}, cap={'compare_point': 0.15})
engine.plot(show_marko=True, show_capm=True)
engine.pprint(show_marko=True, show_capm=True)
