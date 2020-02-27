"""
This is main file that initiates the portfolio engine
Signed off: Hiren Chalodiya <chalodiya.1@iitj.ac.in>
            Mayank Raj <raj.6@iitj.ac.in>
            Darsh Agrawal <agrawal.7@iitj.ac.in>
"""

from yahoo import YahooFinanceData
from datetime import datetime
from engine import PyfolioEngine


# These 25 stocks are taken from United States Market
stock_code = [
    'MSFT', # Microsoft
    'RS', # Reliance
    'GOOGL', # Google
    'AAPL', #Apple
    'AMZN', #Amazon
    'TSLA', #Tesla
    'NFLX', #netflix
    'FB', #Facebook
    'GS', # goldman sachs
    'JPM', # jp morgan chase
    'MS', # morgan stanley
    'DIS', # disney
    'WMT', #walmart
    'TXN', # texas instruments
    'HPE', # hewlet packard
    'IBM', #ibm
    'INTC', # intel
    'NVDA', #nvidia
    'MA',  # mastercard
    'TCS.NS',
    'SQ',
    'CODX',
    'TDOC',
    'IBIO',
    'PYPL',
]


if __name__ == "__main__":
    # Fetch Data
    data = YahooFinanceData(stock_code, fromdate=datetime(2019, 1, 1), todate=datetime(2020, 1, 1))
    data.prepare()

    # Prepare engine to fire 🔥 !!(The engine will calculate the bullet for general parameters)
    engine = PyfolioEngine(data.data, 0.9, 0.0633, marko_mu_max=2, marko_mu_min=-0.3, marko_mu_gap=0.02)
    engine.plot()
