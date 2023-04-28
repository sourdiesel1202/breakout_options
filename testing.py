import os
import time
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime
#from application.app import database
from application.app import strategies
#from application.app import toolbox

ts = time.time()
#db = database.Database()
#db.load_data()
te = time.time()
print(te-ts, 'seconds to load db')
