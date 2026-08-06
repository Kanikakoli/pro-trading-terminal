import pandas as pd

# -------------------------------------------------------
# SCANNER ENGINE
# -------------------------------------------------------

def classify_trade(signal, confidence):

    if "STRONG BUY" in signal:
        trade_type = "INTRADAY BUY"

    elif signal == "★★★★ BUY":
        trade_type = "BUY"

    elif "SELL" in signal:
        trade_type = "SELL"

    else:
        trade_type = "HOLD"

    return trade_type


# -------------------------------------------------------
# HERO ZERO SCANNER
# -------------------------------------------------------

def hero_zero(option_df):

    if option_df is None or len(option_df) == 0:
        return pd.DataFrame()

    df = option_df.copy()

    ce = df[
        (df["CE LTP"] > 5) &
        (df["CE LTP"] < 50)
    ]

    pe = df[
        (df["PE LTP"] > 5) &
        (df["PE LTP"] < 50)
    ]

    ce = ce.sort_values(
        by="CE OI",
        ascending=False
    ).head(5)

    pe = pe.sort_values(
        by="PE OI",
        ascending=False
    ).head(5)

    return {
        "CALLS": ce,
        "PUTS": pe
    }


# -------------------------------------------------------
# SCALPING ENGINE
# -------------------------------------------------------

def scalping(indicator):

    score = 0

    if indicator["RSI"] > 60:
        score += 20

    if indicator["ADX"] > 25:
        score += 20

    if indicator["EMA9"] > indicator["EMA20"]:
        score += 20

    if indicator["MACD"] > 0:
        score += 20

    if indicator["VWAP"] < indicator["EMA9"]:
        score += 20

    if score >= 80:

        return {

            "Trade": "SCALPING BUY",

            "Confidence": score

        }

    return {

        "Trade": "WAIT",

        "Confidence": score

    }


# -------------------------------------------------------
# BTST SCANNER
# -------------------------------------------------------

def btst(indicator, option_data):

    score = 0

    if indicator["EMA20"] > indicator["EMA50"]:
        score += 20

    if indicator["ADX"] > 25:
        score += 20

    if indicator["RSI"] > 55:
        score += 20

    if option_data:

        if option_data["PCR"] > 1:
            score += 20

    if score >= 70:

        return {

            "Trade": "BTST BUY",

            "Score": score

        }

    return {

        "Trade": "NO TRADE",

        "Score": score

    }


# -------------------------------------------------------
# MARKET STRENGTH
# -------------------------------------------------------

def market_strength(indicator, option_data):

    strength = 0

    strength += indicator["RSI"]

    strength += indicator["ADX"]

    if option_data:

        strength += option_data["PCR"] * 20

    strength = round(strength / 3, 2)

    if strength >= 70:

        status = "VERY STRONG"

    elif strength >= 55:

        status = "BULLISH"

    elif strength >= 45:

        status = "NEUTRAL"

    else:

        status = "WEAK"

    return {

        "Strength": strength,

        "Status": status

      }
