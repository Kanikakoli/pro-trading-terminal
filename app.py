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
refresh = st.sidebar.slider(
    "Auto Refresh (sec)",
    5,
    60,
    15
)

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
    df = pd.DataFrame()
    df = safe_history(symbol, timeframe)

    if not df.empty and len(df) > 0:

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
# ----------------------------------------------------
# AI TRADE RECOMMENDATION
# ----------------------------------------------------

st.subheader("🤖 AI Trade Recommendation")

if not df.empty:

    latest = df.iloc[-1]

    score = 0
    reasons = []

    # ---------------- TREND ----------------

    if latest["EMA20"] > latest["EMA50"]:
        score += 20
        reasons.append("✅ EMA20 above EMA50")

    else:
        score -= 20
        reasons.append("❌ EMA20 below EMA50")

    # ---------------- RSI ----------------

    if 55 <= latest["RSI"] <= 70:
        score += 20
        reasons.append("✅ Healthy RSI")

    elif latest["RSI"] > 70:
        score -= 10
        reasons.append("⚠️ Overbought")

    elif latest["RSI"] < 35:
        score += 10
        reasons.append("✅ Oversold Bounce")

    # ---------------- MACD ----------------

    if latest["MACD"] > latest["MACD_SIGNAL"]:
        score += 20
        reasons.append("✅ MACD Bullish")

    else:
        score -= 20
        reasons.append("❌ MACD Bearish")

    # ---------------- ADX ----------------

    if latest["ADX"] > 25:
        score += 20
        reasons.append("✅ Strong Trend")

    else:
        reasons.append("⚠️ Weak Trend")

    # ---------------- VWAP ----------------

    if latest["Close"] > latest["VWAP"]:
        score += 20
        reasons.append("✅ Above VWAP")

    else:
        score -= 20
        reasons.append("❌ Below VWAP")

    # ---------------- SIGNAL ----------------

    if score >= 70:
        signal = "🟢 STRONG BUY"

    elif score >= 40:
        signal = "🟢 BUY"

    elif score <= -40:
        signal = "🔴 STRONG SELL"

    elif score <= -20:
        signal = "🔴 SELL"

    else:
        signal = "🟡 HOLD"

    confidence = min(95, round(50 + abs(score) * 0.6))

    c1, c2 = st.columns(2)

    with c1:
        st.metric("AI Signal", signal)

    with c2:
        st.metric("Confidence", f"{confidence}%")

    st.write("### AI Analysis")

    for item in reasons:
        st.write(item)
# ----------------------------------------------------
# AI TRADE SETUP
# ----------------------------------------------------

st.subheader("🎯 AI Trade Setup")

if not df.empty:

    entry = round(latest["Close"], 2)

    atr = latest["ATR"]

    if "BUY" in signal:

        stop = round(entry - 1.5 * atr, 2)

        target1 = round(entry + 2 * atr, 2)

        target2 = round(entry + 3 * atr, 2)

    elif "SELL" in signal:

        stop = round(entry + 1.5 * atr, 2)

        target1 = round(entry - 2 * atr, 2)

        target2 = round(entry - 3 * atr, 2)

    else:

        stop = None
        target1 = None
        target2 = None

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Entry", entry)

    with c2:
        st.metric("Stop Loss", stop)

    with c3:
        st.metric("Target 1", target1)

    with c4:
        st.metric("Target 2", target2)
