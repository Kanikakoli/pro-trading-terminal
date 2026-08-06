import plotly.graph_objects as go
from plotly.subplots import make_subplots


# --------------------------------------------------------
# CANDLESTICK CHART
# --------------------------------------------------------

def candlestick_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        )
    )

    if "EMA_9" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["EMA_9"],
                mode="lines",
                name="EMA 9"
            )
        )

    if "EMA_20" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["EMA_20"],
                mode="lines",
                name="EMA 20"
            )
        )

    if "VWAP" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["VWAP"],
                mode="lines",
                name="VWAP"
            )
        )

    fig.update_layout(
        template="plotly_white",
        height=550,
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    return fig


# --------------------------------------------------------
# RSI CHART
# --------------------------------------------------------

def rsi_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["RSI"],
            name="RSI"
        )
    )

    fig.add_hline(y=70)

    fig.add_hline(y=30)

    fig.update_layout(
        template="plotly_white",
        height=250,
        margin=dict(l=10, r=10, t=20, b=10)
    )

    return fig


# --------------------------------------------------------
# MACD CHART
# --------------------------------------------------------

def macd_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MACD"],
            name="MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MACD_SIGNAL"],
            name="Signal"
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=250,
        margin=dict(l=10, r=10, t=20, b=10)
    )

    return fig


# --------------------------------------------------------
# OPTION CHAIN OI CHART
# --------------------------------------------------------

def oi_chart(option_df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=option_df["Strike"],
            y=option_df["CE OI"],
            name="Call OI"
        )
    )

    fig.add_trace(
        go.Bar(
            x=option_df["Strike"],
            y=option_df["PE OI"],
            name="Put OI"
        )
    )

    fig.update_layout(
        barmode="group",
        template="plotly_white",
        height=450,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    return fig


# --------------------------------------------------------
# MARKET DASHBOARD
# --------------------------------------------------------

def dashboard_gauge(score):

    fig = go.Figure()

    fig.add_trace(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "AI Confidence"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "green"}

            }

        )

    )

    fig.update_layout(height=320)

    return fig
