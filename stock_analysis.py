import ast, os, re, time
import requests
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from IPython.display import Markdown, display
from datetime import timedelta, datetime, date
from util import validate_dates

from plots import create_candlestick_chart, create_comparison_chart
from lucerna import Lucerna


def get_stock_info(symbol):
    """
    Get general stock info, about the company and prices info.

    parameters
    ----------
    symbol: str
    """
    ticker = yf.Ticker(symbol)
    stock_info = {
        "company_name": ticker.info['longName']
        ,"country": ticker.info['country']
        ,"sector": ticker.info['sector']
        ,"industry": ticker.info['industry']
        ,"business_summary": ticker.info['longBusinessSummary']
        ,"currency": ticker.info['financialCurrency']
        ,"stock_exch": ticker.info['fullExchangeName']
    }
    end_date = date.today()
    st_date = end_date - timedelta(days=183)
    stock_price_df = get_stock_price(ticker, st_date, end_date,
                                      interval='1d', timezone=False)
    stock_info['stock_price_df'] = stock_price_df
    
    return stock_info

def get_stock_price(ticker, st_date, end_date, 
                    interval='1d', timezone=False):
    stock_price_df = ticker.history(start=st_date,
                                     end=end_date, interval='1d')
    if not timezone:
        stock_price_df.index = stock_price_df.index.tz_localize(None)
    return stock_price_df