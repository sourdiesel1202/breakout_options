print(__name__)
import pandas as pd

strategy_name = 'Golden Cross'
days_to_backtest = 1

def golden_cross(df):
    close = df.loc[:, df.columns.get_level_values(1).isin(['Close'])].droplevel(1, axis='columns')
    high = df.loc[:, df.columns.get_level_values(1).isin(['High'])].droplevel(1, axis='columns')
    low = df.loc[:, df.columns.get_level_values(1).isin(['Low'])].droplevel(1, axis='columns')
    sma200 = close.rolling(200).mean()
    sma50 = close.rolling(50).mean()
    # crossover
    xo = (sma50 < sma200) & (((sma50 - sma50.shift(1)) + sma50) > sma200)
    xu = (sma50 > sma200) & ((sma50 - (sma50.shift(1) - sma50)) < sma200)
    # find out if previous day was successful
    calls_hit = xo.shift(1) & (close.shift(1) < high)
    puts_hit = xu.shift(1) & (close.shift(1) > low)
    df = pd.concat([xo,xu,calls_hit,puts_hit], axis=1, keys=['xo','xu','calls_hit','puts_hit']).swaplevel(axis=1)
    return df