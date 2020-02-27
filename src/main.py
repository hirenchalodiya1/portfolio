from yahoo import YahooFinanceData
from datetime import datetime
from engine import PyfolioEngine


stock_code = [
    'MSFT', # Microsoft
    'RS', # Reliance
    'GOOGL', # Google
    'AAPL',
    'AMZN',
    'TSLA',
    'NFLX',
    'FB',
    'GS',
    'JPM',
    'MS',
    'TTM',
    'V',
    'TXN',
    'GE',
    'UNH',
    'GM',
    'F',
    'KO',
    'JNJ',
    'PEP',
    'PG',
    'DIS',
    'WMT',
    'CL'

]
# Fetch data
data = YahooFinanceData(stock_code, fromdate=datetime(2019, 9, 1), todate=datetime(2020, 2, 1))
data.prepare()

# Let engine handlw rest of it !!
engine = PyfolioEngine(data.data, 0.20, 0.0633, marko_mu_max=0.35)
engine.plot()
