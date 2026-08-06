import pandas as pd

try:
    from nsepython import option_chain
except ImportError:
    option_chain = None


# -------------------------------------------------------
# FETCH LIVE OPTION CHAIN
# -------------------------------------------------------

def fetch_option_chain(symbol="NIFTY"):

    if option_chain is None:
        return None

    try:

        data = option_chain(symbol)

        records = data["records"]["data"]

        rows = []

        total_call_oi = 0
        total_put_oi = 0

        max_call_oi = 0
        max_put_oi = 0

        call_resistance = None
        put_support = None

        for item in records:

            strike = item["strikePrice"]

            ce = item.get("CE", {})
            pe = item.get("PE", {})

            call_oi = ce.get("openInterest", 0)
            put_oi = pe.get("openInterest", 0)

            total_call_oi += call_oi
            total_put_oi += put_oi

            if call_oi > max_call_oi:
                max_call_oi = call_oi
                call_resistance = strike

            if put_oi > max_put_oi:
                max_put_oi = put_oi
                put_support = strike

            rows.append({

                "Strike": strike,

                "CE LTP": ce.get("lastPrice", 0),

                "CE OI": call_oi,

                "CE Chg OI": ce.get("changeinOpenInterest", 0),

                "PE LTP": pe.get("lastPrice", 0),

                "PE OI": put_oi,

                "PE Chg OI": pe.get("changeinOpenInterest", 0)

            })

        df = pd.DataFrame(rows)

        pcr = round(total_put_oi / total_call_oi, 2) if total_call_oi else 0

        return {

            "option_chain": df,

            "PCR": pcr,

            "Support": put_support,

            "Resistance": call_resistance,

            "Call OI": max_call_oi,

            "Put OI": max_put_oi

        }

    except Exception as e:

        return {

            "error": str(e)

        }


# -------------------------------------------------------
# MARKET INTERPRETATION
# -------------------------------------------------------

def interpret_market(pcr):

    if pcr >= 1.30:
        return "★★★★★ Strong Bullish"

    elif pcr >= 1.00:
        return "★★★★ Bullish"

    elif pcr >= 0.80:
        return "★★★ Neutral"

    elif pcr >= 0.60:
        return "★★ Bearish"

    else:
        return "★★★★★ Strong Bearish"
