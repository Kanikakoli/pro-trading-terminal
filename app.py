"""
=========================================================
PRO AI TRADING TERMINAL
Version 3.0
Professional Dashboard
=========================================================
"""

import streamlit as st
import pandas as pd

from core.market_data import market_snapshot, safe_history
from core.indicators import add_indicators
from core.scanner import scanner_dataframe

from core.option_chain import (
    get_option_chain,
    pcr,
    support,
    resistance
)

from core.risk_manager import (
    calculate_position_size,
    risk_reward
)

from components.chart import candlestick_chart


# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="PRO AI Trading Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

.main{
    background:#0E1117;
}

div[data-testid="metric-container"]{
    background:#1E1E1E;
    border-radius:12px;
    padding:18px;
    border:1px solid #2E2E2E;
}

h1,h2,h3{
    color:white;
}

</style>
""",unsafe_allow_html=True)

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("📈 PRO AI TRADING TERMINAL")

st.caption("Professional AI Trading Dashboard")

st.divider()
# ----------------------------------------------------
# LIVE MARKET
# ----------------------------------------------------

c1,c2,c3,c4=st.columns(4)

try:

    nifty=market_snapshot("NIFTY")
    bank=market_snapshot("BANKNIFTY")
    sensex=market_snapshot("SENSEX")
    reliance=market_snapshot("RELIANCE")

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

    with c4:
        st.metric(
            "RELIANCE",
            reliance["price"],
            f'{reliance["change"]}%'
        )

except:

    st.error("Unable to fetch Live Market.")

st.divider()

# ----------------------------------------------------
# AI MARKET SCANNER
# ----------------------------------------------------

st.subheader("🔥 AI Market Scanner")

scanner=scanner_dataframe()

if not scanner.empty:

    st.dataframe(
        scanner,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("Scanner data unavailable.")

st.divider()
# ----------------------------------------------------
# LIVE CHART & AI ANALYSIS
# ----------------------------------------------------

st.subheader("📈 Live Chart & AI Analysis")

left, right = st.columns([2, 1])

with left:

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
            use_container_width=True
        )

with right:

    st.subheader("📊 Latest Indicators")

    if not df.empty:

        latest = df.iloc[-1]

        st.metric("Price", round(latest["Close"], 2))
        st.metric("EMA20", round(latest["EMA20"], 2))
        st.metric("EMA50", round(latest["EMA50"], 2))
        st.metric("EMA200", round(latest["EMA200"], 2))
        st.metric("RSI", round(latest["RSI"], 2))
        st.metric("ADX", round(latest["ADX"], 2))
        st.metric("VWAP", round(latest["VWAP"], 2))
st.divider()
