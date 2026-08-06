"""
=========================================================
PRO AI TRADING TERMINAL
Professional Chart Component
Version : 1.0
=========================================================
"""

import plotly.graph_objects as go


def candlestick_chart(df, symbol):

    fig = go.Figure()

    fig.add_trace(

        go.Candlestick(

            x=df["Datetime"] if "Datetime" in df.columns else df["Date"],

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            name=symbol

        )

    )

    if "EMA20" in df.columns:

        fig.add_trace(

            go.Scatter(

                x=df["Datetime"] if "Datetime" in df.columns else df["Date"],

                y=df["EMA20"],

                name="EMA20",

                line=dict(width=1)

            )

        )

    if "EMA50" in df.columns:

        fig.add_trace(

            go.Scatter(

                x=df["Datetime"] if "Datetime" in df.columns else df["Date"],

                y=df["EMA50"],

                name="EMA50",

                line=dict(width=1)

            )

        )

    fig.update_layout(

        height=600,

        xaxis_rangeslider_visible=False,

        template="plotly_dark",

        margin=dict(l=5, r=5, t=30, b=5),

        legend_orientation="h",

        title=f"{symbol} Price Chart"

    )

    return fig
