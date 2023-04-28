print(__name__)
import pandas as pd

strategy_name = 'Breakout (Longer Term)'
days_to_backtest = 3

def breakout_mod(df):
    # assign variables
    high = df.loc[:, df.columns.get_level_values(1).isin(['High'])].droplevel(1, axis='columns')
    low = df.loc[:, df.columns.get_level_values(1).isin(['Low'])].droplevel(1, axis='columns')
    close = df.loc[:, df.columns.get_level_values(1).isin(['Close'])].droplevel(1, axis='columns')
    #
    upper = high * (1 + 4 * (high - low) / (high + low))
    lower = low * (1 - 4 * (high - low) / (high + low))
    upper_band = upper.rolling(20).mean()
    lower_band = lower.rolling(20).mean()
    sma20 = close.rolling(20).mean()
    #
    xo = (
        (close > upper_band)
        & (close.shift(1) > upper_band.shift(1))
        & (close.shift(2) < upper_band.shift(2))
        & (close > sma20)
    )
    xu = (
        (close < lower_band)
        & (close.shift(1) < lower_band.shift(1))
        & (close.shift(2) > lower_band.shift(2))
        & (close < sma20)
    )
    # find out if previous day was successful
    # shift should be rolling 5 day window, but will not execute in 5 days
    # it would be best to find out all XO/XU in the previous 5 days and check rolling 5 max
    calls_hit = xo.shift(5) & (high.rolling(5).max() > close.shift(5))
    puts_hit = xu.shift(5) & (low.rolling(5).min() < close.shift(5))
    df = pd.concat([xo,xu,calls_hit,puts_hit], axis=1, keys=['xo','xu','calls_hit','puts_hit']).swaplevel(axis=1)
    return df