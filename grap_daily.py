from requests_html import HTMLSession
from dateutil import parser as date_parser
import datetime
import timeit
import pandas as pd
import time
import glob

def stringcell2number(x):
    return x.split(":")[1]

def is_date_parsing(date_str):
    try:
        return bool(date_parser.parse(date_str))
    except ValueError:
        return False

date_str = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y/%m/%d')
date_str2 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')

session = HTMLSession()
r = session.get('https://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk')
hiddens = r.html.find('input[name=__VIEWSTATE]', first=True).attrs.get('value')
hiddens1 = r.html.find('input[name=__EVENTVALIDATION]', first=True).attrs.get('value')
hiddens2 = r.html.find('input[name=__VIEWSTATEGENERATOR]', first=True).attrs.get('value')

#date_str = '2021/' + t_month + '/' + t_day
if is_date_parsing(date_str):
    filename_str = date_str2+'_mutual.csv'
    payload = {
        '__VIEWSTATE': hiddens,
        '__EVENTVALIDATION': hiddens1,
        '__VIEWSTATEGENERATOR': hiddens2,
        'today': date_str2,
        'sortBy': 'stockcode',
        'sortDirection': 'asc',
        'txtShareholdingDate': date_str,
        'btnSearch': 'Search'
        }

    r = session.post('https://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk', data=payload)

    try:
        df=pd.DataFrame(pd.read_html(r.html.html)[1])
        df1 = df.iloc[:,[0,2,3]]
        df1 = df1.applymap(stringcell2number)
        df1['Date'] = pd.to_datetime(date_str, format='%Y/%m/%d', errors='ignore')
        df1.to_csv(filename_str, index=False, header=False)
    except:
        print("No data on ", date_str)