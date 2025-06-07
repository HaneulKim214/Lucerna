from datetime import datetime, date, timedelta

import pandas as pd


def df_to_DFloader(df, date_col='date'):
    """
    Convert dataframe into python code where a dictionary is loaded as a Pandas df for
    LLM input.

    example:
    df -> "pd.DataFrame({name:['helen', james], 'age':[33,23]})"

    parameters
    ----------
    df: pd.DataFrame

    return
    ------
    dfloader: str, text version of python code for creating dataframe
    """

    if isinstance(df.index, pd.DatetimeIndex):
        df = (df.reset_index()
               .astype({"index":str}) # convert datetime column to string
               .rename(columns={"index":date_col})
             )

    dfloader = f"pd.DataFrame({df.to_dict(orient='list')})"
    return dfloader

def validate_dates(st_date, end_date):
    """
    Check
    1. whether dates are in %Y-%m-%d (a.k.a. yyyy-mm-dd format).
    2. 0000-00-00 < st_date <= end_date <= today's date.

    :param st_date: str
    :param end_date: str
    :return: None
    """
    try:
        st_date = datetime.strptime(st_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError as e:
        raise Exception(f"Date format error: {e}")

    if st_date < date(1,1,1):
        raise ValueError("Start date must later than 0001-01-01")
    # +1 as a buffer just in case of timezone difference
    if end_date > date.today() + timedelta(days=1):
        raise ValueError("End date canoot be in the future")
    if st_date > end_date:
        raise ValueError("Start date cannot be after end date")

