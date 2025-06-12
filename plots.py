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
        xaxis_rangeslider_visible=False,
        # Make plot responsive to container size
        autosize=True,
        # Dark theme colors
        plot_bgcolor='#1E1E1E',  # Dark background
        paper_bgcolor='#1E1E1E',  # Dark background for the whole figure
        font=dict(color='#FFFFFF'),  # White text
        # Style the axes
        xaxis=dict(
            gridcolor='#333333',
            zerolinecolor='#333333'
        ),
        yaxis=dict(
            gridcolor='#333333',
            zerolinecolor='#333333'
        )
    )
    return fig


def create_comparison_chart(df, title, chart_type='scatter'):
    """
    Create a chart that compares columns.
    x-axis will be df.index

    parameters
    ----------
    df: pd.DataFrame
    """
    charts = {"scatter":go.Scatter, "bar":go.Bar}
    chart_options = list(charts.keys())
    if chart_type not in chart_options:
        raise ValueError(f"{chart_type} does not exist. Choose from {chart_options}")
    
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(
            charts[chart_type](
                x=df.index,
                y=df[col],
                name=col
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        xaxis_rangeslider_visible=False
    )
    return fig