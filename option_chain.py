"""
=========================================================
PRO AI TRADING TERMINAL
Option Chain Engine
Version : 1.0
=========================================================
"""

import pandas as pd

try:
    from nsepython import option_chain
except:
    option_chain = None


def get_option_chain(symbol="NIFTY"):

    if option_chain is None:
        return pd.DataFrame()

    try:

        data = option_chain(symbol)

        records = []

        for row in data["records"]["data"]:

            strike = row.get("strikePrice")

            ce = row.get("CE")
            pe = row.get("PE")

            records.append({

                "Strike": strike,

                "CE_OI": ce["openInterest"] if ce else 0,

                "CE_COI": ce["changeinOpenInterest"] if ce else 0,

                "CE_LTP": ce["lastPrice"] if ce else 0,

                "PE_OI": pe["openInterest"] if pe else 0,

                "PE_COI": pe["changeinOpenInterest"] if pe else 0,

                "PE_LTP": pe["lastPrice"] if pe else 0,

            })

        return pd.DataFrame(records)

    except Exception:

        return pd.DataFrame()


def calculate_pcr(df):

    if df.empty:
        return None

    put_oi = df["PE_OI"].sum()

    call_oi = df["CE_OI"].sum()

    if call_oi == 0:
        return None

    return round(put_oi / call_oi, 2)


def highest_call_oi(df):

    if df.empty:
        return None

    row = df.loc[df["CE_OI"].idxmax()]

    return {
        "Strike": row["Strike"],
        "OI": row["CE_OI"]
    }


def highest_put_oi(df):

    if df.empty:
        return None

    row = df.loc[df["PE_OI"].idxmax()]

    return {
        "Strike": row["Strike"],
        "OI": row["PE_OI"]
    }


def market_sentiment(pcr):

    if pcr is None:
        return "UNKNOWN"

    if pcr > 1.3:
        return "BULLISH"

    if pcr < 0.7:
        return "BEARISH"

    return "NEUTRAL"


def option_summary(symbol="NIFTY"):

    df = get_option_chain(symbol)

    if df.empty:

        return {

            "PCR": None,

            "Sentiment": "Unavailable",

            "HighestCallOI": None,

            "HighestPutOI": None,

            "Data": df

        }

    pcr = calculate_pcr(df)

    return {

        "PCR": pcr,

        "Sentiment": market_sentiment(pcr),

        "HighestCallOI": highest_call_oi(df),

        "HighestPutOI": highest_put_oi(df),

        "Data": df

                   }
