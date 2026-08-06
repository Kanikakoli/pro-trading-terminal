import pandas as pd
import ta

# --------------------------------------------------
# TECHNICAL INDICATORS ENGINE
# --------------------------------------------------

def calculate_indicators(df):

    if df is None or len(df) < 50:
        return None

    df = df.copy()

    # ----------------------------
    # EMA
    # ----------------------------

    df["EMA_9"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=9
    ).ema_indicator()

    df["EMA_20"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=20
    ).ema_indicator()

    df["EMA_50"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=50
    ).ema_indicator()

    # ----------------------------
    # RSI
    # ----------------------------

    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()

    # ----------------------------
    # MACD
    # ----------------------------

    macd = ta.trend.MACD(df["Close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    # ----------------------------
    # ADX
    # ----------------------------

    adx = ta.trend.ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )

    df["ADX"] = adx.adx()

    # ----------------------------
    # ATR
    # ----------------------------

    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )

    df["ATR"] = atr.average_true_range()

    # ----------------------------
    # Bollinger Bands
    # ----------------------------

    bb = ta.volatility.BollingerBands(df["Close"])

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_LOWER"] = bb.bollinger_lband()

    # ----------------------------
    # VWAP
    # ----------------------------

    vwap = ta.volume.VolumeWeightedAveragePrice(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        volume=df["Volume"]
    )

    df["VWAP"] = vwap.volume_weighted_average_price()

    return df


# --------------------------------------------------
# AI SIGNAL ENGINE
# --------------------------------------------------

def generate_signal(df):

    last = df.iloc[-1]

    score = 0

    # EMA Trend
    if last["EMA_9"] > last["EMA_20"]:
        score += 20

    if last["EMA_20"] > last["EMA_50"]:
        score += 20

    # RSI
    if 55 <= last["RSI"] <= 70:
        score += 15

    # MACD
    if last["MACD"] > last["MACD_SIGNAL"]:
        score += 20

    # VWAP
    if last["Close"] > last["VWAP"]:
        score += 15

    # ADX
    if last["ADX"] > 25:
        score += 10

    if score >= 80:
        signal = "★★★★★ STRONG BUY"

    elif score >= 60:
        signal = "★★★★ BUY"

    elif score >= 40:
        signal = "★★★ HOLD"

    else:
        signal = "★★ SELL"

    return {
        "Signal": signal,
        "Score": score,
        "RSI": round(last["RSI"], 2),
        "ADX": round(last["ADX"], 2),
        "ATR": round(last["ATR"], 2),
        "VWAP": round(last["VWAP"], 2),
        "EMA9": round(last["EMA_9"], 2),
        "EMA20": round(last["EMA_20"], 2),
        "EMA50": round(last["EMA_50"], 2),
        "MACD": round(last["MACD"], 2)
  }
