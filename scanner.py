"""
=========================================================
PRO AI TRADING TERMINAL
Professional Stock Scanner
Version : 1.0
=========================================================
"""

from core.market_data import safe_history
from core.indicators import add_indicators, latest_indicators
from core.ai_engine import generate_signal


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

            "Price": ind["Price"],

            "Signal": ai["Signal"],

            "Confidence": ai["Confidence"],

            "RSI": ind["RSI"],

            "ADX": ind["ADX"],

            "Reasons": ", ".join(ai["Reasons"])

        }

    except:

        return None


def scan_market():

    results = []

    for symbol in WATCHLIST:

        item = scan_symbol(symbol)

        if item:

            results.append(item)

    results.sort(

        key=lambda x: x["Confidence"],

        reverse=True

    )

    return results


def top_buys(results):

    return [

        x for x in results

        if x["Signal"] in [

            "BUY",

            "STRONG BUY"

        ]

    ]


def top_sells(results):

    return [

        x for x in results

        if x["Signal"] in [

            "SELL",

            "STRONG SELL"

        ]

    ]
