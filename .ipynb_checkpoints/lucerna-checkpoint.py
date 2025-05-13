import os, time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from datetime import timedelta, datetime
from util import validate_dates



class Lucerna:
    def __init__(self, llm, version="gemini-2.0-flash"):
        self.model = configure_llm(llm)


    def 