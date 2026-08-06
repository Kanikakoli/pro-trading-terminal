"""
=========================================================
PRO AI TRADING TERMINAL
AI Trading Engine
Version : 2.0
=========================================================
"""

def generate_signal(ind):

    score = 0
    reasons = []

    price = ind["Price"]

    # ---------------------------------
    # EMA Trend (25 Points)
    # ---------------------------------

    if ind["EMA20"] > ind["EMA50"] > ind["EMA200"]:
        score += 25
        reasons.append("Strong EMA Uptrend")

    elif ind["EMA20"] < ind["EMA50"] < ind["EMA200"]:
        score -= 25
        reasons.append("Strong EMA Downtrend")

    # ---------------------------------
    # RSI (15 Points)
    # ---------------------------------

    if 55 <= ind["RSI"] <= 70:
        score += 15
        reasons.append("Bullish RSI")

    elif 30 <= ind["RSI"] <= 45:
        score -= 15
        reasons.append("Bearish RSI")

    elif ind["RSI"] > 75:
        reasons.append("Overbought")

    elif ind["RSI"] < 25:
        reasons.append("Oversold")

    # ---------------------------------
    # MACD (20 Points)
    # ---------------------------------

    if ind["MACD"] > ind["MACD_SIGNAL"]:
        score += 20
        reasons.append("MACD Bullish")

    else:
        score -= 20
        reasons.append("MACD Bearish")

    # ---------------------------------
    # VWAP (15 Points)
    # ---------------------------------

    if price > ind["VWAP"]:
        score += 15
        reasons.append("Above VWAP")

    else:
        score -= 15
        reasons.append("Below VWAP")

    # ---------------------------------
    # ADX (15 Points)
    # ---------------------------------

    if ind["ADX"] > 25:
        score += 15
        reasons.append("Strong Trend")

    else:
        reasons.append("Weak Trend")

    # ---------------------------------
    # Bollinger Bands (10 Points)
    # ---------------------------------

    if price < ind["BB_LOWER"]:
        score += 10
        reasons.append("Near Lower Band")

    elif price > ind["BB_UPPER"]:
        score -= 10
        reasons.append("Near Upper Band")

    # ---------------------------------
    # Final Signal
    # ---------------------------------

    if score >= 60:
        signal = "STRONG BUY"

    elif score >= 30:
        signal = "BUY"

    elif score <= -60:
        signal = "STRONG SELL"

    elif score <= -30:
        signal = "SELL"

    else:
        signal = "HOLD"

    confidence = min(abs(score), 95)

    # ---------------------------------
    # Risk Levels
    # ---------------------------------

    atr = ind["ATR"]

    if signal in ["BUY", "STRONG BUY"]:

        entry = round(price, 2)
        sl = round(price - (1.5 * atr), 2)
        target1 = round(price + (2 * atr), 2)
        target2 = round(price + (4 * atr), 2)

    elif signal in ["SELL", "STRONG SELL"]:

        entry = round(price, 2)
        sl = round(price + (1.5 * atr), 2)
        target1 = round(price - (2 * atr), 2)
        target2 = round(price - (4 * atr), 2)

    else:

        entry = round(price, 2)
        sl = "-"
        target1 = "-"
        target2 = "-"

    return {

        "Signal": signal,

        "Confidence": confidence,

        "Score": score,

        "Entry": entry,

        "SL": sl,

        "Target1": target1,

        "Target2": target2,

        "Reasons": reasons

        }
