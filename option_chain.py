"""
=========================================================
PRO AI TRADING TERMINAL
Option Chain Engine
Version 1.0
=========================================================
"""

import requests
import pandas as pd


HEADERS = {

    "User-Agent":
    "Mozilla/5.0"

}


def get_option_chain():

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    session = requests.Session()

    session.get(
        "https://www.nseindia.com",
        headers=HEADERS,
        timeout=10
    )

    data = session.get(
        url,
        headers=HEADERS,
        timeout=10
    ).json()

    records = data["records"]["data"]

    rows = []

    for item in records:

        strike = item["strikePrice"]

        ce = item.get("CE", {})

        pe = item.get("PE", {})

        rows.append({

            "Strike": strike,

            "Call OI": ce.get("openInterest", 0),

            "Call ChgOI": ce.get("changeinOpenInterest", 0),

            "Call LTP": ce.get("lastPrice", 0),

            "Put LTP": pe.get("lastPrice", 0),

            "Put ChgOI": pe.get("changeinOpenInterest", 0),

            "Put OI": pe.get("openInterest", 0)

        })

    return pd.DataFrame(rows)


def pcr(df):

    put = df["Put OI"].sum()

    call = df["Call OI"].sum()

    if call == 0:
        return 0

    return round(put / call, 2)


def support(df):

    row = df.sort_values(

        "Put OI",

        ascending=False

    ).iloc[0]

    return row["Strike"]


def resistance(df):

    row = df.sort_values(

        "Call OI",

        ascending=False

    ).iloc[0]

    return row["Strike"]
