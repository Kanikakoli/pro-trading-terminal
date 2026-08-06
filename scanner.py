"""
=========================================================
PRO AI TRADING TERMINAL
Professional Scanner Engine
Version : 2.0
=========================================================
"""

import pandas as pd

from core.market_data import safe_history
from core.indicators import add_indicators, latest_indicators
from core.ai_engine import generate_signal


# -------------------------------------------------------
# Watchlist
# -------------------------------------------------------

WATCHLIST = [

    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",

    "NIFTY",
    "BANKNIFTY"

]


# -------------------------------------------------------
# Scan Single Symbol
# -------------------------------------------------------

def scan_symbol(symbol):

    try:

        df = safe_history(symbol, "15m")

        if df.empty:
            return None

        df = add_indicators(df)

        ind = latest_indicators(df)

        ai = generate_signal(ind)

        return {

            "Symbol": symbol,

            "Price": ai["Entry"],

            "Signal": ai["Signal"],

            "Confidence": ai["Confidence"],

            "Score": ai["Score"],

            "Entry": ai["Entry"],

            "SL": ai["SL"],

            "Target1": ai["Target1"],

            "Target2": ai["Target2"],

            "RSI": ind["RSI"],

            "ADX": ind["ADX"],

            "VWAP": ind["VWAP"],

            "Reasons": " | ".join(ai["Reasons"])

        }

    except Exception:

        return None


# -------------------------------------------------------
# Scan Entire Market
# -------------------------------------------------------

def scan_market():

    results = []

    for symbol in WATCHLIST:

        item = scan_symbol(symbol)

        if item:
            results.append(item)

    if len(results) == 0:
        return []

    results = sorted(

        results,

        key=lambda x: x["Confidence"],

        reverse=True

    )

    return results


# -------------------------------------------------------
# BUY LIST
# -------------------------------------------------------

def top_buys():

    data = scan_market()

    return [

        x for x in data

        if x["Signal"] in [

            "BUY",

            "STRONG BUY"

        ]

    ]


# -------------------------------------------------------
# SELL LIST
# -------------------------------------------------------

def top_sells():

    data = scan_market()

    return [

        x for x in data

        if x["Signal"] in [

            "SELL",

            "STRONG SELL"

        ]

    ]


# -------------------------------------------------------
# DataFrame
# -------------------------------------------------------

def scanner_dataframe():

    data = scan_market()

    if len(data) == 0:

        return pd.DataFrame()

    return pd.DataFrame(data)
