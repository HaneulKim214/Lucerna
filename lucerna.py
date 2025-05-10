import os, time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from datetime import timedelta, datetime
from util import validate_dates

print("Welcome, I am Lucerna, your customized investment advisor!")
company_ticker = input("What company would you like to know about. Provide ticker symbol:")
start_date = input("Start date (yyyy-mm-dd): ")
end_date = input("End date (yyyy-mm-dd): ")

# check validity of inputs
validate_dates(start_date, end_date)
print(f"Analysis beginning for {company_ticker} from {start_date} ~ {end_date}")



# i) Generate plot, tables for stock prices and fundamental analysis
stock_price_df = yf.download([company_ticker]
                             ,start=start_date
                             ,end=end_date
                             ,interval='1d'
                             ,threads=True)
ticker = yf.Ticker(company_ticker)
business_summary = ticker.info['longBusinessSummary']
currency = ticker.info['currency']
stock_exch = ticker.info['exchange']



