import streamlit as st
import pandas as pd
from datetime import datetime

# Import our modules
from market_data import get_live_market_data
from indicators import calculate_indicators, generate_signal
from option_chain import fetch_option_chain, interpret_market
from ai_engine import generate_trade, risk_management
from scanner import hero_zero, scalping, btst, market_strength
from charts import (
    candlestick_chart,
    rsi_chart,
    macd_chart,
    oi_chart,
    dashboard_gauge,
)

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="PRO AI Trading Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------

PASSWORD = "pro12345"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔒 PRO AI Trading Terminal")

    pwd = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if pwd == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Wrong Password")

    st.stop()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("⚙ Settings")

symbol = st.sidebar.selectbox(
    "Index",
    [
        "NIFTY",
        "BANKNIFTY"
    ]
)

interval = st.sidebar.selectbox(
    "Timeframe",
    [
        "5m",
        "15m",
        "30m",
        "1h",
        "1d"
    ]
)

refresh = st.sidebar.slider(
    "Refresh (sec)",
    5,
    60,
    15
)

st.sidebar.success("Backend Connected")

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("🚀 PRO AI Trading Terminal")

st.caption(
    f"Live Market | {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.divider()
