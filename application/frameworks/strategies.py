import pandas as pd
import pandas_ta as ta

inventory = [
    'get_golden_cross',
    'get_breakout',
    #'get_adx_cross',
    'get_breakout_mod',
]

def get_golden_cross(df):
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

def get_breakout(df):
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
        & (close > sma20)
    )
    xu = (
        (close < lower_band)
        & (close.shift(1) < lower_band.shift(1))
        & (close < sma20)
    )
    # find out if previous day was successful
    calls_hit = xo.shift(1) & (high > close.shift(1))
    puts_hit = xu.shift(1) & (low < close.shift(1))
    df = pd.concat([xo,xu,calls_hit,puts_hit], axis=1, keys=['xo','xu','calls_hit','puts_hit']).swaplevel(axis=1)
    return df

def get_adx_cross(df):
    symbols = df.columns.get_level_values(0).unique().sort_values(ascending=True)
    adx = pd.DataFrame()
    for symbol in symbols:
        adx_single = df[symbol].ta.adx()
        adx = pd.concat([adx, adx_single], axis=1)
    #adx = df.ta.adx()
    
    lt_adx_20 = adx['ADX_14'] < 20
    gt_0day_1day = adx['ADX_14'] > adx['ADX_14'].shift(1)
    gt_1day_2day = adx['ADX_14'].shift(1) > adx['ADX_14'].shift(2)
    less_0day_1day = adx['ADX_14'] - adx['ADX_14'].shift(1)
    plus_0day_diff = adx['ADX_14'] + less_0day_1day
    gt_plus_20 = plus_0day_diff > 20
    gt_dmp_dmn = adx['DMP_14'] > adx['DMN_14']
    gt_dmn_dmp = adx['DMN_14'] > adx['DMP_14']
    
    dff = pd.concat([
        adx['ADX_14'],
        adx['ADX_14'].shift(1),
        lt_adx_20,
        gt_0day_1day,
        gt_1day_2day,
        less_0day_1day,
        plus_0day_diff,
        gt_plus_20,
        gt_dmp_dmn,
        gt_dmn_dmp,
    ], axis=1)
    dff.columns = [
        'adx',
        'adx_1day',
        'lt_adx_20',
        'gt_0day_1day',
        'gt_1day_2day',
        'less_0day_1day',
        'plus_0day_diff',
        'gt_plus_20',
        'gt_dmp_dmn',
        'gt_dmn_dmp',
    ]
    df['xo'] = (
        # ADX is less than 20
        lt_adx_20 &
        # upward trend of ADX
        gt_0day_1day &
        # stronger uptrend!
        gt_1day_2day &
        # today plus difference between today and yesterday, is above 20
        gt_plus_20 &
        # DMP is stronger than DMN
        gt_dmp_dmn
    )
    df['xu'] = (
        # ADX is less than 20
        lt_adx_20 &
        # upward trend of ADX
        gt_0day_1day &
        # stronger uptrend!
        gt_1day_2day &
        # today plus difference between today and yesterday, is above 20
        gt_plus_20 &
        # DMN is stronger than DMP
        gt_dmn_dmp
    )
    
    df['calls_hit'] = df['xo'].shift(1) & (df['Close'].shift(1) < df['High'])
    df['puts_hit'] = df['xu'].shift(1) & (df['Close'].shift(1) > df['Low'])
    return df

def get_breakout_mod(df):
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

if __name__ == '__main__':
    ...
