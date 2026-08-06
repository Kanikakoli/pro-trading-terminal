"""
=========================================================
PRO AI TRADING TERMINAL
Professional Charts Engine
Version : 1.0
=========================================================
"""

import plotly.graph_objects as go


def create_chart(df):

    fig = go.Figure()

    # -------------------------
    # Candlestick
    # -------------------------
    fig.add_trace(

        go.Candlestick(

            x=df["Datetime"],

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            name="Price"

        )

    )

    # -------------------------
    # EMA20
    # -------------------------
    fig.add_trace(

        go.Scatter(

            x=df["Datetime"],

            y=df["EMA20"],

            mode="lines",

            name="EMA20"

        )

    )

    # -------------------------
    # EMA50
    # -------------------------
    fig.add_trace(

        go.Scatter(

            x=df["Datetime"],

            y=df["EMA50"],

            mode="lines",

            name="EMA50"

        )

    )

    # -------------------------
    # EMA200
    # -------------------------
    fig.add_trace(

        go.Scatter(

            x=df["Datetime"],

            y=df["EMA200"],

            mode="lines",

            name="EMA200"

        )

    )

    # -------------------------
    # VWAP
    # -------------------------
    fig.add_trace(

        go.Scatter(

            x=df["Datetime"],

            y=df["VWAP"],

            mode="lines",

            name="VWAP"

        )

    )

    # -------------------------
    # Bollinger Bands
    # -------------------------
    fig.add_trace(

        go.Scatter(

            x=df["Datetime"],

            y=df["BB_UPPER"],

            mode="lines",

            name="BB Upper"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["Datetime"],

            y=df["BB_LOWER"],

            mode="lines",

            name="BB Lower"

        )

    )

    # -------------------------
    # Layout
    # -------------------------
    fig.update_layout(

        template="plotly_dark",

        height=700,

        xaxis_rangeslider_visible=False,

        legend_orientation="h",

        margin=dict(

            l=10,

            r=10,

            t=30,

            b=10

        )

    )

    return fig
