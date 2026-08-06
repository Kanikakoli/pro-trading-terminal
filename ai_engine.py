"""
=========================================================
PRO AI TRADING TERMINAL
AI Decision Engine
Version : 1.0
=========================================================
"""


def generate_signal(ind):

    score = 0
    reasons = []

    # -------------------------
    # EMA Trend
    # -------------------------
    if ind["Price"] > ind["EMA20"]:
        score += 10
        reasons.append("Price above EMA20")

    if ind["EMA20"] > ind["EMA50"]:
        score += 15
        reasons.append("EMA20 above EMA50")

    if ind["EMA50"] > ind["EMA200"]:
        score += 20
        reasons.append("EMA50 above EMA200")

    # -------------------------
    # RSI
    # -------------------------
    if 55 <= ind["RSI"] <= 70:
        score += 15
        reasons.append("Healthy RSI")

    elif ind["RSI"] < 35:
        score -= 10
        reasons.append("Oversold")

    elif ind["RSI"] > 75:
        score -= 15
        reasons.append("Overbought")

    # -------------------------
    # MACD
    # -------------------------
    if ind["MACD"] > ind["MACD_SIGNAL"]:
        score += 15
        reasons.append("Bullish MACD")

    else:
        score -= 10
        reasons.append("Bearish MACD")

    # -------------------------
    # ADX
    # -------------------------
    if ind["ADX"] > 25:
        score += 10
        reasons.append("Strong Trend")

    # -------------------------
    # VWAP
    # -------------------------
    if ind["Price"] > ind["VWAP"]:
        score += 10
        reasons.append("Above VWAP")

    # -------------------------
    # Bollinger
    # -------------------------
    if ind["Price"] < ind["BB_LOWER"]:
        score += 5
        reasons.append("Near Lower Band")

    if ind["Price"] > ind["BB_UPPER"]:
        score -= 5
        reasons.append("Near Upper Band")

    # -------------------------
    # Final Signal
    # -------------------------

    confidence = min(max(score, 0), 100)

    if confidence >= 85:
        signal = "STRONG BUY"

    elif confidence >= 70:
        signal = "BUY"

    elif confidence >= 45:
        signal = "HOLD"

    elif confidence >= 25:
        signal = "SELL"

    else:
        signal = "STRONG SELL"

    return {
        "Signal": signal,
        "Confidence": confidence,
        "Reasons": reasons
    }
