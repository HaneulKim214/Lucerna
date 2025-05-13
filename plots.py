import pandas as pd
import plotly.graph_objects as go


def create_candlestick_chart(df, name, curr):
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(x=df.index,
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close']))
    fig.update_layout(
        title=f'{name} prices in ({curr})',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    return fig