import os
import json
import time
import datetime
import importlib

import requests_cache
import yfinance as yf
import pandas as pd

from application.app import database
#from application.app import strategies
#from application.app import toolbox

ts = time.time()
db = database.Database()
df = db.load_data()
te = time.time()
print(te-ts, 'seconds to load db')

# errors
#df = yf.download('AAPL', period='max', interval='1d', group_by='ticker', threads=True)

'''
strategy = 'breakout'
strategy_module = importlib.import_module(f'strategy_files.{strategy}')
strategy_fn = getattr(strategy_module, strategy)
results = strategy_fn(df)
picks = toolbox.find_todays_breakout(
    df,
    strategy_fn,
    days=strategy_module.days_to_backtest,
)
'''