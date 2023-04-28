print(__name__)
import pandas as pd
import pandas_ta as ta

strategy_name = 'ADX Cross'
days_to_backtest = 1

def adx_cross(df):
    symbols = df.columns.get_level_values(0).unique().sort_values(ascending=True)
    adx = pd.DataFrame()
    for symbol in symbols:
        adx_single = df[symbol].ta.adx()
        adx_single['Ticker'] = symbol
        adx_single = adx_single.set_index('Ticker', append=True).unstack('Ticker').swaplevel(axis=1)
        adx = pd.concat([adx, adx_single], axis=1)
    #adx = df.ta.adx()

    close = df.loc[:, df.columns.get_level_values(1).isin(['Close'])].droplevel(1, axis='columns')
    high = df.loc[:, df.columns.get_level_values(1).isin(['High'])].droplevel(1, axis='columns')
    low = df.loc[:, df.columns.get_level_values(1).isin(['Low'])].droplevel(1, axis='columns')
    adx_14 = adx.loc[:, adx.columns.get_level_values(1).isin(['ADX_14'])].droplevel(1, axis='columns')
    dmp_14 = adx.loc[:, adx.columns.get_level_values(1).isin(['DMP_14'])].droplevel(1, axis='columns')
    dmn_14 = adx.loc[:, adx.columns.get_level_values(1).isin(['DMN_14'])].droplevel(1, axis='columns')

    lt_adx_20 = adx_14 < 20
    gt_0day_1day = adx_14 > adx_14.shift(1)
    gt_1day_2day = adx_14.shift(1) > adx_14.shift(2)
    less_0day_1day = adx_14 - adx_14.shift(1)
    plus_0day_diff = adx_14 + less_0day_1day
    gt_plus_20 = plus_0day_diff > 20
    gt_dmp_dmn = dmp_14 > dmn_14
    gt_dmn_dmp = dmn_14 > dmp_14

    xo = (
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
    xu = (
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

    calls_hit = xo.shift(1) & (close.shift(1) < high)
    puts_hit = xu.shift(1) & (close.shift(1) > low)
    df = pd.concat([xo,xu,calls_hit,puts_hit], axis=1, keys=['xo','xu','calls_hit','puts_hit']).swaplevel(axis=1)
    return df