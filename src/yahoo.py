"""
To bypass yahoo finance data security first find crumb(api token) from history url
Use sessions to download multiple urls
intervals = {
            bt.TimeFrame.Days: '1d',
            bt.TimeFrame.Weeks: '1wk',
            bt.TimeFrame.Months: '1mo',
        }

This file is used to fetch data from yahoo.finance site and store it in cache in csv format
"""
import requests
import os
import pandas as pd
from datetime import date


CSV_CACHE_FOLDER = '../yahoodata'


class YahooFinanceData:
    def __init__(self, dataname, fromdate, todate, interval='1d'):
        posix = date(1970, 1, 1)

        # args for url
        if type(dataname) is list:
            self.dataname = dataname
        else:
            self.dataname = [dataname]
        self.period1 = int((fromdate.date() - posix).total_seconds())
        self.period2 = int((todate.date() - posix).total_seconds())
        self.interval = interval
        self.urlhist = 'https://finance.yahoo.com/quote/{}/history'
        self.urldown = 'https://query1.finance.yahoo.com/v7/finance/download/{}'

        # request session
        self.sess = requests.Session()
        self.sesskwargs = dict()
        self.retries = 4

        # finance data
        self.data = {}

        # cache data folder
        if not os.path.isdir(CSV_CACHE_FOLDER):
            os.makedirs(CSV_CACHE_FOLDER)

    def prepare(self):
        required = set(self.dataname)

        for dname in self.dataname:
            # data and file
            stock_data = None
            file_name = '{}_{}_{}_{}.csv'.format(dname, self.period1, self.period2, self.interval)
            file_path = os.path.join(CSV_CACHE_FOLDER, file_name)
            error = None
            
            # find in cache first
            if os.path.isfile(file_path):
                print('{} found in cache'.format(dname))
                
                with open(file_path) as f:
                    stock_data = f.read()
                
                required.remove(dname)
                continue

            # history URL to get crumb (API token)
            url = self.urlhist.format(dname)

            crumb = None
            for i in range(self.retries + 1):  # at least once
                resp = self.sess.get(url, **self.sesskwargs)
                if resp.status_code != requests.codes.ok:
                    continue

                txt = resp.text
                i = txt.find('CrumbStore')
                if i == -1:
                    continue
                i = txt.find('crumb', i)
                if i == -1:
                    continue
                istart = txt.find('"', i + len('crumb') + 1)
                if istart == -1:
                    continue
                istart += 1
                iend = txt.find('"', istart)
                if iend == -1:
                    continue

                crumb = txt[istart:iend]
                crumb = crumb.encode('ascii').decode('unicode-escape')
                break

            if crumb is None:
                error = 'crumb not found'
                print('{} {}'.format(dname, error))
                stock_data = None
                continue

            # Download URL 
            urld = self.urldown.format(dname)
            urlargs = []
            urlargs.append('period2={}'.format(self.period2))
            urlargs.append('period1={}'.format(self.period1))
            urlargs.append('interval={}'.format(self.interval))
            urlargs.append('events=history')
            urlargs.append('crumb={}'.format(crumb))
            urld = '{}?{}'.format(urld, '&'.join(urlargs))

            for i in range(self.retries + 1):  # at least once
                resp = self.sess.get(urld, **self.sesskwargs)
                if resp.status_code != requests.codes.ok:
                    continue
                ctype = resp.headers['Content-Type']
                if 'text/csv' not in ctype:
                    error = 'Wrong content type: %s' % ctype
                    continue  # HTML returned? wrong url?
                stock_data = resp.text
                break

            if error:
                print('{} {}'.format(dname, error))
                continue
        
            print('{} downloaded and stored in cache'.format(dname))
            with open(file_path, 'w') as f:
                f.write(stock_data)
            
            required.remove(dname)
        
        if len(required):
            raise ValueError("Not all stockes are downloaded, Run again until I am disappeared")

        self._update()

    def _update(self):
        for dname in self.dataname:
            file_name = '{}_{}_{}_{}.csv'.format(dname, self.period1, self.period2, self.interval)
            file_path = os.path.join(CSV_CACHE_FOLDER, file_name)
            self.data[dname] = pd.read_csv(file_path)['Close']
        self.data = pd.DataFrame.from_dict(self.data)
