"""
=========================================================
PRO AI TRADING TERMINAL
Technical Indicators Engine
Version : 1.0
=========================================================
"""

import pandas as pd
import ta


def add_indicators(df):

    if df.empty:
        return df

    data = df.copy()

    # ------------------------
    # EMA
    # ------------------------
    data["EMA20"] = ta.trend.EMAIndicator(
        close=data["Close"],
        window=20
    ).ema_indicator()

    data["EMA50"] = ta.trend.EMAIndicator(
        close=data["Close"],
        window=50
    ).ema_indicator()

    data["EMA200"] = ta.trend.EMAIndicator(
        close=data["Close"],
        window=200
    ).ema_indicator()

    # ------------------------
    # RSI
    # ------------------------
    data["RSI"] = ta.momentum.RSIIndicator(
        close=data["Close"],
        window=14
    ).rsi()

    # ------------------------
    # MACD
    # ------------------------
    macd = ta.trend.MACD(
        close=data["Close"]
    )

    data["MACD"] = macd.macd()
    data["MACD_SIGNAL"] = macd.macd_signal()
    data["MACD_HIST"] = macd.macd_diff()

    # ------------------------
    # ADX
    # ------------------------
    adx = ta.trend.ADXIndicator(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14
    )

    data["ADX"] = adx.adx()

    # ------------------------
    # ATR
    # ------------------------
    atr = ta.volatility.AverageTrueRange(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14
    )

    data["ATR"] = atr.average_true_range()

    # ------------------------
    # Bollinger Bands
    # ------------------------
    bb = ta.volatility.BollingerBands(
        close=data["Close"],
        window=20,
        window_dev=2
    )

    data["BB_UPPER"] = bb.bollinger_hband()
    data["BB_MIDDLE"] = bb.bollinger_mavg()
    data["BB_LOWER"] = bb.bollinger_lband()

    # ------------------------
    # VWAP
    # ------------------------
    vwap = ta.volume.VolumeWeightedAveragePrice(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        volume=data["Volume"]
    )

    data["VWAP"] = vwap.volume_weighted_average_price()

    return data


# =========================================================
# Latest Indicator Values
# =========================================================

def latest_indicators(df):

    row = df.iloc[-1]

    return {

        "Price": round(row["Close"],2),

        "EMA20": round(row["EMA20"],2),

        "EMA50": round(row["EMA50"],2),

        "EMA200": round(row["EMA200"],2),

        "RSI": round(row["RSI"],2),

        "MACD": round(row["MACD"],2),

        "MACD_SIGNAL": round(row["MACD_SIGNAL"],2),

        "ADX": round(row["ADX"],2),

        "ATR": round(row["ATR"],2),

        "VWAP": round(row["VWAP"],2),

        "BB_UPPER": round(row["BB_UPPER"],2),

        "BB_LOWER": round(row["BB_LOWER"],2)

    }
