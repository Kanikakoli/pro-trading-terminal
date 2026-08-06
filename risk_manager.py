"""
=========================================================
PRO AI TRADING TERMINAL
Professional Risk Manager
Version : 2.0
=========================================================
"""


def calculate_trade(price,
                    stop_loss,
                    capital,
                    risk_percent=1):

    """
    Returns complete position sizing.
    """

    risk_amount = capital * (risk_percent / 100)

    risk_per_share = abs(price - stop_loss)

    if risk_per_share <= 0:

        quantity = 0

    else:

        quantity = int(risk_amount / risk_per_share)

    investment = quantity * price

    return {

        "Capital": round(capital, 2),

        "RiskPercent": risk_percent,

        "RiskAmount": round(risk_amount, 2),

        "Quantity": quantity,

        "Investment": round(investment, 2)

    }


def risk_reward(entry,
                stop_loss,
                target):

    risk = abs(entry - stop_loss)

    reward = abs(target - entry)

    if risk == 0:

        return 0

    return round(reward / risk, 2)


def trailing_stop(signal,
                  current_price,
                  atr):

    """
    ATR Based Trailing Stop
    """

    if signal in ["BUY", "STRONG BUY"]:

        return round(current_price - atr * 1.5, 2)

    elif signal in ["SELL", "STRONG SELL"]:

        return round(current_price + atr * 1.5, 2)

    return current_price


def target_levels(entry,
                  atr,
                  signal):

    if signal in ["BUY", "STRONG BUY"]:

        return {

            "T1": round(entry + atr * 2, 2),

            "T2": round(entry + atr * 4, 2),

            "T3": round(entry + atr * 6, 2)

        }

    elif signal in ["SELL", "STRONG SELL"]:

        return {

            "T1": round(entry - atr * 2, 2),

            "T2": round(entry - atr * 4, 2),

            "T3": round(entry - atr * 6, 2)

        }

    return {

        "T1": entry,

        "T2": entry,

        "T3": entry

    }


def trade_summary(signal,
                  entry,
                  stop_loss,
                  atr,
                  capital=100000,
                  risk_percent=1):

    pos = calculate_trade(
        entry,
        stop_loss,
        capital,
        risk_percent
    )

    targets = target_levels(
        entry,
        atr,
        signal
    )

    rr = risk_reward(
        entry,
        stop_loss,
        targets["T2"]
    )

    trail = trailing_stop(
        signal,
        entry,
        atr
    )

    return {

        **pos,

        **targets,

        "TrailingSL": trail,

        "RiskReward": rr

                    }
