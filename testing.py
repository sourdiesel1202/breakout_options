import os
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from application.app import database
from application.app import strategies
from application.app import toolbox

ts = time.time()
db = database.Database()
db.load_data()
te = time.time()
print(te-ts, 'seconds to load db')

df = db.df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)
#adx = df.ta.adx()
close = db.df.loc[:, db.df.columns.get_level_values(1).isin(['Close'])].droplevel(1, axis='columns')
high = db.df.loc[:, db.df.columns.get_level_values(1).isin(['High'])].droplevel(1, axis='columns')
low = db.df.loc[:, db.df.columns.get_level_values(1).isin(['Low'])].droplevel(1, axis='columns')
adx = ta.adx(db.df['AAPL']['High'], db.df['AAPL']['Low'], db.df['AAPL']['Close'])

idx = []
for symbol in symbols:
    for col in adx.columns:
        idx.append((symbol, col))
#ts = time.time()
#results = strategies.get_breakout_mod(db.df.copy())
#symbols = results.columns.get_level_values(0).unique().sort_values(ascending=True)
#te = time.time()
#print(te-ts, 'seconds to run strategy')

#xo = results.loc[:, results.columns.get_level_values(1).isin(['xo'])].droplevel(1, axis='columns')
#xu = results.loc[:, results.columns.get_level_values(1).isin(['xu'])].droplevel(1, axis='columns')
#picks_xo = xo.loc[:,xo.tail(1).any()].tail(1).columns
#picks_xu = xu.loc[:,xu.tail(1).any()].tail(1).columns
#for pick in picks_xo: print('xo', pick)
#for pick in picks_xu: print('xu', pick)



def run_backtest(db, results, days=1):
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    df = db.join(results)
    df['Profit+'] = (df['High'].shift(-days).rolling(days).max() - df['Close']).where(df['xo'] == True)
    df['Profit-'] = (df['Close'] - df['Low'].shift(-days)).where(df['xu'] == True)
    df[~df['Profit+'].isnull()]
    df[~df['Profit-'].isnull()]
    # mean for crossovers
    xo_avg = df['Profit+'].median()
    xo_days = df['Profit+'].count()
    # mean for crossunders
    xu_avg = df['Profit-'].median()
    xu_days = df['Profit-'].count()
    # total median
    avg = pd.concat([df['Profit+'].dropna(), df['Profit-'].dropna()]).median()
    # total
    xo_days_win = df[df['Profit+'] >= 0]['Profit+'].count()
    xu_days_win = df[df['Profit-'] >= 0]['Profit-'].count()
    xo_days_loss = df[df['Profit+'] < 0]['Profit+'].count()
    xu_days_loss = df[df['Profit-'] < 0]['Profit-'].count()
    xo_days_total = xo_days_win + xo_days_loss
    xu_days_total = xu_days_win + xo_days_loss
    xo_ratio = (xo_days_win / xo_days_total) * 100 if xo_days_total != 0 else 0
    xu_ratio = (xu_days_win / xu_days_total) * 100 if xu_days_total != 0 else 0
    message_dict = {
        'call_ratio': f'{xo_ratio:.2f}%',
        'call_diff': f'{xo_avg:.2f}',
        'put_ratio': f'{xu_ratio:.2f}%',
        'put_diff': f'{xu_avg:.2f}',
    }
    return message_dict

def find_todays_breakout(db, fn):
    results = fn(db)
    symbols = results.columns.get_level_values(0).unique().sort_values(ascending=True)
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    picks = []
    for symbol in symbols:
        if results[symbol].tail(1)['xo'].bool():
            contract_type = 'call'
            cross = 'xo'
        elif results[symbol].tail(1)['xu'].bool():
            contract_type = 'put'
            cross = 'xu'
        else:
            continue
        # ignore multiple breakouts within 4 days
        if list(results[symbol][cross].tail(4)).count(True) > 1: continue
        data_copy = db[symbol].copy()
        strike_float = float(data_copy['Close'].iloc[-1])
        strike = f'{strike_float:.02f}'
        adx = data_copy.ta.adx()
        stochrsi = data_copy.ta.stochrsi()
        adx_uptrend = (adx.tail(1)['ADX_14'] > adx.shift(1).tail(1)['ADX_14']).bool()
        dmi_uptrend = (adx.tail(1)['DMP_14'] > adx.tail(1)['DMN_14']).bool()
        rsi_uptrend = (stochrsi.tail(1)['STOCHRSId_14_14_3_3'] > stochrsi.shift(1)['STOCHRSId_14_14_3_3'].tail(1)).bool()
        pick = all([dmi_uptrend, adx_uptrend, rsi_uptrend]) or all([not dmi_uptrend, not adx_uptrend, rsi_uptrend])
        bt = run_backtest(data_copy, results[symbol].copy())
        picks.append({
                'symbol': symbol,
                'strike': strike,
                'type': contract_type,
                'dmi': dmi_uptrend,
                'rsi': rsi_uptrend,
                'adx': adx_uptrend,
                'pick': pick,
                'bt': bt,
            })
    return picks

#ts = time.time()
#picks = find_todays_breakout(db.df.copy(), strategies.get_breakout_mod)
#te = time.time()
#print(te-ts, 'seconds to find breakout')