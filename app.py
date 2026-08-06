"""
=========================================================
PRO AI TRADING TERMINAL
Dashboard
Version : 1.0
=========================================================
"""

import streamlit as st
import pandas as pd
from core.market_data import safe_history
from core.indicators import add_indicators
from components.chart import candlestick_chart

from core.market_data import market_snapshot
from core.scanner import scanner_dataframe

st.set_page_config(
    page_title="PRO AI TRADING TERMINAL",
    page_icon="📈",
    layout="wide"
)

st.title("📈 PRO AI TRADING TERMINAL")

st.caption("Live Market Dashboard")

st.divider()

# =========================
# LIVE MARKET
# =========================

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

# =========================
# AI SCANNER
# =========================

st.subheader("🔥 AI Trade Scanner")

df = scanner_dataframe()

if len(df):

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

else:

    st.warning("No signals available.")

st.divider()

# =========================
# TOP BUY
# =========================

if len(df):

    buy = df[df["Signal"].isin(["BUY", "STRONG BUY"])]

    if len(buy):

        st.success("Best Trade Right Now")

        st.dataframe(

            buy.head(5),

            use_container_width=True,

            hide_index=True

        )

st.divider()

st.caption("Professional AI Trading Terminal")
