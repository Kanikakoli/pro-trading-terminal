"""
==========================================
Risk Management
==========================================
"""

def calculate_position_size(capital, risk_percent, entry, stoploss):

    risk_amount = capital * (risk_percent / 100)

    risk_per_share = abs(entry - stoploss)

    if risk_per_share == 0:
        return 0

    quantity = int(risk_amount / risk_per_share)

    return quantity


def risk_reward(entry, target, stoploss):

    reward = abs(target - entry)
    risk = abs(entry - stoploss)

    if risk == 0:
        return 0

    return round(reward / risk, 2)
