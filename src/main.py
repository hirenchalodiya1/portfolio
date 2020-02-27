from yahoo import YahooFinanceData
from datetime import datetime
from engine import PyfolioEngine
import quandl


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
    
    # 'BA'   

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
    # Fetch data
    # data = YahooFinanceData(new_stocks, fromdate=datetime(2016, 12, 1), todate=datetime(2016, 12, 31))
    # data.prepare()
    quandl.ApiConfig.api_key = 'NMgz64DRkZaB-kfxENfJ'
    data = quandl.get_table('WIKI/PRICES', ticker = stock_code,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': '2016-12-1', 'lte': '2016-12-31' }, paginate=True)

    # reorganise data pulled by setting date as index with
    # columns of tickers and their corresponding adjusted prices
    clean = data.set_index('date')
    table = clean.pivot(columns='ticker')

    # Let engine handlw rest of it !!
    engine = PyfolioEngine(table, 0.05, 0.0, marko_mu_max=5, marko_mu_min=-1, marko_mu_gap=0.1)
    engine.plot()
