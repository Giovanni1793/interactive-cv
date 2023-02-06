import pandas as pd
import datetime as dt
import json
import requests
import yfinance as yf
data = pd.read_csv('tickers_filtered.csv')

valid_tickers = []

for ticker in data['Ticker']:
    df = yf.Ticker(ticker).history(period = '1d')
    if len(df) >=1:
        valid_tickers.append(ticker)
    else:
        pass
new_data = data[data['Ticker'].isin(valid_tickers)]

new_data.to_csv('valid_tickers.csv')
