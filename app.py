import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================
# PAGE CONFIGURATION
# ==========================

st.set_page_config(
    page_title="PRO AI Trading Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# IMPORT MODULES
# ==========================

from core.market_data import get_live_indices
from core.option_chain import option_summary
from core.scanner import scan_market

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

.main{
    background:#0E1117;
}

.card{
background:#1A1D24;
padding:18px;
border-radius:15px;
border:1px solid #2B3139;
margin-bottom:15px;
}

.title{
font-size:28px;
font-weight:bold;
color:white;
}

.small{
color:#B0B8C1;
font-size:14px;
}

.buy{
color:#00E676;
font-weight:bold;
}

.sell{
color:#FF5252;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("📈 PRO TERMINAL")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Scanner",
        "Intraday",
        "Hero Zero",
        "Scalping",
        "BTST",
        "Option Chain",
        "Charts",
        "Global",
        "Mutual Funds"
    ]
)

st.sidebar.markdown("---")

refresh = st.sidebar.slider(
    "Auto Refresh (seconds)",
    5,
    60,
    15
)

st.sidebar.success("Status : LIVE")

# ==========================
# HEADER
# ==========================

st.markdown(
f"""
<div class="title">
PRO AI TRADING TERMINAL
</div>

<div class="small">

{datetime.now().strftime("%d %b %Y | %H:%M:%S")}

</div>

""",
unsafe_allow_html=True
)

st.divider()

# ==========================
# DASHBOARD
# ==========================

if page=="Dashboard":

    st.subheader("Live Market")

    indices=get_live_indices()

    cols=st.columns(len(indices))

    for col,(name,data) in zip(cols,indices.items()):

        change=data["change"]

        emoji="🟢" if change>=0 else "🔴"

        col.metric(
            name,
            f"{data['price']:.2f}",
            f"{change:.2f}%"
        )

    st.divider()

    left,right=st.columns([2,1])

    with left:

        st.subheader("🔥 AI Market Scanner")

        scan=scan_market()

        if len(scan):

            df=pd.DataFrame(scan)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("No signals available.")

    with right:

        st.subheader("Option Chain Summary")

        summary=option_summary("NIFTY")

        st.metric(
            "PCR",
            summary["PCR"]
        )

        st.metric(
            "Sentiment",
            summary["Sentiment"]
        )

        if summary["HighestCallOI"]:

            st.write(
                "Highest Call OI",
                summary["HighestCallOI"]["Strike"]
            )

        if summary["HighestPutOI"]:

            st.write(
                "Highest Put OI",
                summary["HighestPutOI"]["Strike"]
            )

    st.divider()

    st.info("Professional Dashboard Version 3.0")
