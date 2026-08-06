"""
=========================================================
PRO AI TRADING TERMINAL
Master Watchlist
Version : 1.0
=========================================================
"""

# -------------------------
# Indices
# -------------------------

INDICES = [

    "NIFTY",
    "BANKNIFTY",
    "SENSEX",
    "FINNIFTY",
    "MIDCPNIFTY"

]

# -------------------------
# NIFTY 50 (Major Stocks)
# -------------------------

NIFTY50 = [

    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "LT",
    "ITC",
    "AXISBANK",
    "KOTAKBANK",
    "BHARTIARTL",
    "HCLTECH",
    "MARUTI",
    "M&M",
    "NTPC",
    "POWERGRID",
    "SUNPHARMA",
    "ULTRACEMCO",
    "TITAN",
    "BAJFINANCE"

]

# -------------------------
# High Volume F&O Stocks
# -------------------------

FNO = [

    "ADANIENT",
    "ADANIPORTS",
    "TATASTEEL",
    "JSWSTEEL",
    "HINDALCO",
    "COALINDIA",
    "BEL",
    "BHEL",
    "ONGC",
    "SAIL",
    "IOC",
    "PNB",
    "CANBK",
    "INDIGO",
    "DLF",
    "LODHA"

]

# -------------------------
# Complete Watchlist
# -------------------------

WATCHLIST = list(

    dict.fromkeys(

        INDICES +

        NIFTY50 +

        FNO

    )

)
