"""
=========================================================
PRO AI TRADING TERMINAL
Risk Management Engine
Version : 1.0
=========================================================
"""


def calculate_trade(entry,
                    capital=100000,
                    risk_percent=2):

    """
    Returns complete trade plan
    """

    risk_amount = capital * (risk_percent / 100)

    stoploss = round(entry * 0.97, 2)

    target1 = round(entry * 1.03, 2)

    target2 = round(entry * 1.06, 2)

    target3 = round(entry * 1.10, 2)

    risk_per_share = max(entry - stoploss, 0.01)

    quantity = int(risk_amount / risk_per_share)

    investment = round(quantity * entry, 2)

    reward = target2 - entry

    rr = round(reward / risk_per_share, 2)

    return {

        "Entry": entry,

        "StopLoss": stoploss,

        "Target1": target1,

        "Target2": target2,

        "Target3": target3,

        "RiskAmount": round(risk_amount, 2),

        "Quantity": quantity,

        "Investment": investment,

        "RiskReward": rr

    }


def trailing_stop(entry,
                  current_price,
                  current_sl):

    """
    Dynamic trailing stop
    """

    profit = current_price - entry

    if profit >= entry * 0.10:

        return round(current_price * 0.97, 2)

    elif profit >= entry * 0.05:

        return round(current_price * 0.98, 2)

    elif profit >= entry * 0.03:

        return round(entry, 2)

    return current_sl


def trade_status(current_price,
                 stoploss,
                 target1,
                 target2,
                 target3):

    if current_price <= stoploss:
        return "STOP LOSS HIT"

    if current_price >= target3:
        return "TARGET 3 ACHIEVED"

    if current_price >= target2:
        return "TARGET 2 ACHIEVED"

    if current_price >= target1:
        return "TARGET 1 ACHIEVED"

    return "TRADE ACTIVE"
