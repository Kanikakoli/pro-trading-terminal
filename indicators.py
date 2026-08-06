"""
=========================================================
PRO AI TRADING TERMINAL
Indicator Engine
Version : 2.0
=========================================================
"""

import pandas as pd
import ta


def add_indicators(df):

    if df.empty:
        return df

    df = df.copy()

    # ---------- EMA ----------
    df["EMA20"] = ta.trend.ema_indicator(df["Close"], 20)
    df["EMA50"] = ta.trend.ema_indicator(df["Close"], 50)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], 200)

    # ---------- RSI ----------
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

    # ---------- MACD ----------
    macd = ta.trend.MACD(df["Close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    # ---------- ADX ----------
    adx = ta.trend.ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )

    df["ADX"] = adx.adx()

    # ---------- ATR ----------
    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )

    df["ATR"] = atr.average_true_range()

    # ---------- VWAP ----------
    vwap = ta.volume.VolumeWeightedAveragePrice(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        volume=df["Volume"]
    )

    df["VWAP"] = vwap.volume_weighted_average_price()

    # ---------- Bollinger ----------
    bb = ta.volatility.BollingerBands(df["Close"])

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df


def latest_indicators(df):

    row = df.iloc[-1]

    return {

        "Price": round(row["Close"], 2),

        "EMA20": round(row["EMA20"], 2),

        "EMA50": round(row["EMA50"], 2),

        "EMA200": round(row["EMA200"], 2),

        "RSI": round(row["RSI"], 2),

        "MACD": round(row["MACD"], 2),

        "MACD_SIGNAL": round(row["MACD_SIGNAL"], 2),

        "ADX": round(row["ADX"], 2),

        "ATR": round(row["ATR"], 2),

        "VWAP": round(row["VWAP"], 2),

        "BB_UPPER": round(row["BB_UPPER"], 2),

        "BB_LOWER": round(row["BB_LOWER"], 2)

    }
