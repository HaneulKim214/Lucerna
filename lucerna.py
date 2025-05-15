import os, time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from datetime import timedelta, datetime
from util import validate_dates
from config import configure_llm
from prompts import prompt_templates as pt


class Lucerna:
    def __init__(self, llm='gemini', version="gemini-2.0-flash"):
        """

        :param llm:
        :param version:
        """
        self.llm_model = configure_llm(llm, version)

    def explain_service(self, company, custom_prompt=None):
        """

        :return:
        llm response: txt
        """
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = pt.prompt_service_info.format(company=company)
        return self.llm_model.generate_content(prompt)

