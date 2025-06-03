import os, time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from IPython.display import Markdown, display
from datetime import timedelta, datetime, date
from util import validate_dates

from plots import create_candlestick_chart
from lucerna import Lucerna
from dotenv import load_dotenv

"""
## i) stock prices and fundamental analysis
1. Stock price plot (5y so that user can dynamically change ranges)
2. Basic information of stock.
<br>2.1. History, vision, industry, service products, and future)
<br>2.2. Fundamental analysis with competitors (EPS, marketcap, PER, inside investments, institution investments etc...). Market share.



Keep on updating:
<br>2.1. daily reading news and summarizing news related to them.
<br>2.2. Once in a while when data changes.
"""

print("Welcome, I am Lucerna, your customized investment advisor!")
ticker = input("What company would you like to know about. Provide ticker symbol:")


ticker = yf.Ticker(ticker)
stock_info = {
    "company_name": ticker.info['longName']
    ,"country": ticker.info['country']
    ,"sector": ticker.info['sector']
    ,"industry": ticker.info['industry']
    ,"business_summary": ticker.info['longBusinessSummary']
    ,"currency": ticker.info['financialCurrency']
    ,"stock_exch": ticker.info['fullExchangeName']}

# n_years = 1
# end_date = date.today()
# st_date = end_date - timedelta(days=365*n_years)
# stock_price_df = ticker.history(start=st_date, end=end_date, interval='1d')
#
# # ??? How to render interative version to web...?
#
# fig_price = create_candlestick_chart(stock_price_df, stock_info['company_name'], stock_info['currency'])
# fig_price.show()
#
# print(f"""
# Company: {stock_info['company_name']}
# Sector: {stock_info['sector']}
# Industry: {stock_info['industry']}
# Currency: {stock_info['currency']}
# Traded in: {stock_info['stock_exch']}
#
# About:
# {stock_info['business_summary']}
# """)

lucerna = Lucerna('openai', "o4-mini")
resp = lucerna.explain_service(stock_info['company_name'])
print(resp)