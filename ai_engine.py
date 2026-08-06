from datetime import datetime


# -------------------------------------------------------
# AI TRADE ENGINE
# -------------------------------------------------------

def generate_trade(indicator_data, option_data=None):

    score = 0
    reasons = []

    # -----------------------------
    # EMA Trends
    # -----------------------------
    if indicator_data["EMA9"] > indicator_data["EMA20"]:
        score += 15
        reasons.append("EMA 9 > EMA 20")

    if indicator_data["EMA20"] > indicator_data["EMA50"]:
        score += 15
        reasons.append("EMA 20 > EMA 50")

    # -----------------------------
    # RSI
    # -----------------------------
    rsi = indicator_data["RSI"]

    if 55 <= rsi <= 70:
        score += 15
        reasons.append("Healthy RSI")

    elif rsi > 70:
        score -= 5
        reasons.append("Overbought")

    elif rsi < 35:
        score -= 10
        reasons.append("Oversold")

    # -----------------------------
    # MACD
    # -----------------------------
    if indicator_data["MACD"] > 0:
        score += 15
        reasons.append("MACD Positive")

    # -----------------------------
    # ADX
    # -----------------------------
    if indicator_data["ADX"] > 25:
        score += 10
        reasons.append("Strong Trend")

    # -----------------------------
    # VWAP
    # -----------------------------
    if indicator_data["VWAP"] < indicator_data["EMA9"]:
        score += 10
        reasons.append("Above VWAP")

    # -----------------------------
    # PCR
    # -----------------------------
    if option_data:

        pcr = option_data["PCR"]

        if 0.90 <= pcr <= 1.20:
            score += 10
            reasons.append("Healthy PCR")

        elif pcr > 1.20:
            score += 5
            reasons.append("Bullish PCR")

        elif pcr < 0.70:
            score -= 10
            reasons.append("Bearish PCR")

    # -----------------------------
    # Final Signal
    # -----------------------------
    if score >= 80:

        signal = "★★★★★ STRONG BUY"

    elif score >= 65:

        signal = "★★★★ BUY"

    elif score >= 45:

        signal = "★★★ HOLD"

    elif score >= 30:

        signal = "★★ SELL"

    else:

        signal = "★★★★★ STRONG SELL"

    confidence = min(score, 100)

    return {

        "signal": signal,

        "confidence": confidence,

        "score": score,

        "reasons": reasons,

        "generated": datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    }


# -------------------------------------------------------
# RISK MANAGEMENT
# -------------------------------------------------------

def risk_management(entry_price):

    sl = round(entry_price * 0.97, 2)

    target1 = round(entry_price * 1.03, 2)

    target2 = round(entry_price * 1.06, 2)

    target3 = round(entry_price * 1.10, 2)

    rr = round((target2-entry_price)/(entry_price-sl),2)

    return {

        "Entry": entry_price,

        "StopLoss": sl,

        "Target1": target1,

        "Target2": target2,

        "Target3": target3,

        "RiskReward": rr

          }
