import pandas as pd
import datetime as dt
import json
import requests
import yfinance as yf


def get_data_yahoo(tickers):

    dataframes = []
    print(f'-------------retrieving data for {tickers} .... -----------------')
    for i in tickers:
        try:
            g = yf.Ticker(i).history(period = 'max')
            g = g[['Close']]
            g = g.rename(columns = {'Close': i})
            g = g.dropna(axis = 0)
            g = g[[i]]
            dataframes.append(g)
        except:
            pass
    print('retrieving completed')
    df = pd.concat(dataframes, axis=1)
    print(df.head())
    return df

def basket_type_map(data,basket_type):
    if basket_type == 'worst-of':
        return data.min(axis = 1)[-1]
    elif basket_type == 'best-of':
        return data.max(axis = 1)[-1]
    else:
        return data.sum(axis = 1) [-1]


def backtest_setup(bt_tenor, basket, tenor, basket_type):
    """We retrieve historical data for the underlyings"""
    print('-------------backtest setup initiated -----------------')
    df = get_data_yahoo(basket)
    print('-------------retrieving from yahoo.... -----------------')

    """ dates manipulation - we find the last day from which perfomance can be computed
    we define the acquisition dates from [today - backtest tenor; last_aquisition_date]
    """

    last_acquisition_date = dt.datetime.today() - dt.timedelta(weeks=52 * tenor)
    first_acquisition_date = dt.datetime.today() - dt.timedelta(weeks=52 * bt_tenor)
    list_acquisition_date = list(
    df.loc[first_acquisition_date:last_acquisition_date].index)

    list_valuation_date = list(
    df.loc[last_acquisition_date:dt.datetime.today()].index)

    w_basket = []
    for starting_date in list_acquisition_date:
        end_backtest = starting_date + dt.timedelta(weeks=52 * tenor)

        # Compute returns over the period
        data = df.loc[starting_date:end_backtest]
        data = data.divide(data.iloc[0] / 100)

        w_basket.append(basket_type_map(data,basket_type))

    r = pd.DataFrame()
    r['Acquisition Date'] = list_acquisition_date
    r['Performance'] = w_basket
    r['Performance'] = r['Performance'] - 100

    return r
