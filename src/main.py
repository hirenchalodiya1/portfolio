from yahoo import YahooFinanceData
from datetime import datetime
from engine import PyfolioEngine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


stock_code = [
    'MSFT', # Microsoft
    'RS', # Reliance
    'GOOGL', # Google
    # 'GOOG',
    'AAPL', #Apple
    'AMZN', #Amazon
    'TSLA', #Tesla
    'NFLX', #netflix
    'FB', #Facebook
    'GS', # goldman sachs
    'JPM', # jp morgan chase
    'MS', # morgan stanley
    # 'TTM',
    # 'F',
    # 'KO',
    # 'JNJ',
    # 'PEP',
    # 'PG',
    'DIS', # disney
    'WMT', #walmart
    'TXN', # texas instruments
    # 'INFY', #infosys
    'HPE', # hewlet packard
    'IBM', #ibm
    'INTC', # intel
    'NVDA', #nvidia
    # 'UBER', #uber
    # 'NTNX', # nutanix
    'MA',  # mastercard
    'TCS.NS',
    # 'WIPRO.NS',
    # 'CRISIL.BO',
    # 'LAOPALA.BO',
    # 'BOSCHLTD.NS'
    'SQ',
    'CODX',
    'TDOC',
    'IBIO',
    'PYPL'

]
new_stocks = [
    'AAPL',
    'MSFT',
    'AMZN',
    'GOOGL',
    'ADBE',
    'ORCL',
    'SAP',
    'NVDA',
    'CSCO',
    'QCOM',
    'VMW',
    'HTHIY',
    'CRM',
    'IBM',
    "CTSH",
    'JPM',
    'MA',
    'AMD',
    'INTC',
    'MS',
    'GS',
    'WMT',
    'AXP',
    'BAC',
    'C'
]

if __name__ == "__main__":
    data = YahooFinanceData(stock_code, fromdate=datetime(2019, 1, 1), todate=datetime(2020, 1, 1))
    data.prepare()
    engine = PyfolioEngine(data.data, 0.9, 0.0633, marko_mu_max=2, marko_mu_min=-0.3, marko_mu_gap=0.02)
    engine.plot()
