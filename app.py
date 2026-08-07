"""
=========================================================
PRO AI TRADING TERMINAL
Dashboard
Version : 2.0
=========================================================
"""

import streamlit as st
import pandas as pd
from core.option_chain import (
    get_option_chain,
    pcr,
    support,
    resistance
)

from core.market_data import market_snapshot, safe_history
from core.indicators import add_indicators
from core.scanner import scanner_dataframe
from components.chart import candlestick_chart
from core.option_chain import *


# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="PRO AI Trading Terminal",
    page_icon="📈",
    layout="wide"
)

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("📈 PRO AI Trading Terminal")

st.caption("Professional AI Based Trading Dashboard")

st.divider()

# ----------------------------------------------------
# LIVE MARKET
# ----------------------------------------------------

c1, c2, c3 = st.columns(3)

nifty = market_snapshot("NIFTY")
bank = market_snapshot("BANKNIFTY")
sensex = market_snapshot("SENSEX")

with c1:
    st.metric(
        "NIFTY",
        nifty["price"],
        f'{nifty["change"]}%'
    )

with c2:
    st.metric(
        "BANKNIFTY",
        bank["price"],
        f'{bank["change"]}%'
    )

with c3:
    st.metric(
        "SENSEX",
        sensex["price"],
        f'{sensex["change"]}%'
    )

st.divider()

# ----------------------------------------------------
# AI MARKET SCANNER
# ----------------------------------------------------

st.subheader("🔥 AI Scanner")

scanner = scanner_dataframe()

if len(scanner):

    st.dataframe(
        scanner,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No signals available.")

st.divider()

# ----------------------------------------------------
# TOP BUY
# ----------------------------------------------------

st.subheader("🚀 Top BUY Opportunities")

if len(scanner):

    buy = scanner[
        scanner["Signal"].isin(
            [
                "BUY",
                "STRONG BUY"
            ]
        )
    ]

    st.dataframe(
        buy.head(5),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Buy Signals")

st.divider()

# ----------------------------------------------------
# TOP SELL
# ----------------------------------------------------

st.subheader("🔻 Top SELL Opportunities")

if len(scanner):

    sell = scanner[
        scanner["Signal"].isin(
            [
                "SELL",
                "STRONG SELL"
            ]
        )
    ]

    st.dataframe(
        sell.head(5),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Sell Signals")

st.divider()

# ----------------------------------------------------
# LIVE CHART
# ----------------------------------------------------

st.subheader("📈 Live Candlestick Chart")

col1, col2 = st.columns(2)

with col1:

    symbol = st.selectbox(

        "Select Symbol",

        [

            "NIFTY",
            "BANKNIFTY",
            "RELIANCE",
            "TCS",
            "INFY",
            "HDFCBANK",
            "ICICIBANK",
            "SBIN"

        ]

    )

with col2:

    timeframe = st.selectbox(

        "Timeframe",

        [

            "5m",
            "15m",
            "30m",
            "1h",
            "1d"

        ]

    )

df = safe_history(symbol, timeframe)

if not df.empty:

    df = add_indicators(df)

    fig = candlestick_chart(df, symbol)

    st.plotly_chart(
        fig,
        use
st.plotly_chart(
    fig,
    use_container_width=True
)

else:

    st.error("No market data available.")
st.divider()

st.subheader("📊 Live Option Chain")

try:

    oc = get_option_chain()

    st.dataframe(
        oc.tail(15),
        use_container_width=True,
        hide_index=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("PCR", pcr(oc))

    with col2:
        st.metric("Support", support(oc))

    with col3:
        st.metric("Resistance", resistance(oc))

except Exception as e:
    st.warning(f"Option Chain unavailable: {e}")
