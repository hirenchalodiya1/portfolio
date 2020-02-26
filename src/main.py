from yahoo import YahooFinanceData
from datetime import datetime
from engine import PyfolioEngine


stock_code = [
    'MSFT', # Microsoft
    'RS', # Reliance
    'GOOGL', # Google
    'HEROMOTOCO.NS',
    'KOTAKBANK.NS',
    'ICICIBANK.NS',
    'IDEA.NS',
    'YESBANK.NS',
    'TATAPOWER.NS',
    'ONGC.NS',
    'ITC.NS',
    'AXISBANK.NS',
    'AAPL',
    'AMZN',
    'TSLA',
    'NFLX',
    'FB',
    'GS',
    # 'JPM',
    'MS',
    # 'TTM',
    'TCS.NS',
    "MARUTI.NS",
    'V',
    'TXN',
    # 'GE',
    # 'UNH',
    'OIL.NS',
    # '2222.SR',
    'HINDUNILVR.NS'
]
# Fetch data
data = YahooFinanceData(stock_code, fromdate=datetime(2019, 9, 1), todate=datetime(2020, 2, 1))
data.prepare()

# Let engine handlw rest of it !!
engine = PyfolioEngine(data.data, 0.20, 0.05, marko_mu_max=0.35)
engine.plot()
