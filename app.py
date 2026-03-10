import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="DevoteFX PRO", layout="wide")

st.title("📊 DevoteFX PRO Market Scanner")

# -------- MENU --------

menu = st.tabs([
"💰 Big Money",
"🌡️ Heatmap",
"🪤 Trap",
"💧 Liquidity",
"📦 Order Block",
"💎 Smart Money",
"📥 Accumulation",
"📊 Volume",
"📈 Technical",
"🚀 Breakout",
"🎯 Pivot"
])

# -------- CONTROLS --------

col1,col2,col3,col4 = st.columns([2,1,1,1])

with col1:
    market = st.selectbox("Market",["Nifty 50"])

with col2:
    min_cr = st.number_input("Min ₹Cr",value=4)

with col3:
    run = st.button("▶ RUN SCAN")

with col4:
    auto = st.checkbox("⏱ Auto")

# -------- STOCK LIST --------

stocks = [
"RELIANCE.NS","TCS.NS","INFY.NS",
"HDFCBANK.NS","ICICIBANK.NS",
"HINDUNILVR.NS","SBIN.NS","LT.NS"
]

# -------- DOWNLOAD DATA --------

@st.cache_data(ttl=300)
def load_data():

    return yf.download(
        tickers=stocks,
        period="5d",
        interval="15m",
        group_by="ticker",
        progress=False
    )

if run or auto:

    data = load_data()

    big_money=[]
    breakout=[]
    volume_spike=[]

    for s in stocks:

        try:

            df=data[s]

            price=df["Close"].iloc[-1]
            volume=df["Volume"].iloc[-1]
            avg=df["Volume"].rolling(20).mean().iloc[-2]

            trade_value=price*volume/10000000

            high20=df["High"].rolling(20).max().iloc[-2]

            if trade_value>min_cr:
                big_money.append([s.replace(".NS",""),price,round(trade_value,2)])

            if price>high20:
                breakout.append([s.replace(".NS",""),price])

            if volume>3*avg:
                volume_spike.append([s.replace(".NS",""),volume])

        except:
            pass

# -------- TAB CONTENT --------

with menu[0]:

    st.subheader("💰 Big Money")

    if run:

        df=pd.DataFrame(big_money,columns=["Symbol","Price","₹ Cr"])

        st.dataframe(df)

with menu[7]:

    st.subheader("📊 Volume Spike")

    if run:

        df=pd.DataFrame(volume_spike,columns=["Symbol","Volume"])

        st.dataframe(df)

with menu[9]:

    st.subheader("🚀 Breakouts")

    if run:

        df=pd.DataFrame(breakout,columns=["Symbol","Price"])

        st.dataframe(df)

# -------- OTHER TABS --------

with menu[1]:
    st.info("Heatmap scanner coming soon")

with menu[2]:
    st.info("Trap detection coming soon")

with menu[3]:
    st.info("Liquidity zones coming soon")

with menu[4]:
    st.info("Order block detection coming soon")

with menu[5]:
    st.info("Smart money flow coming soon")

with menu[6]:
    st.info("Accumulation scanner coming soon")

with menu[8]:
    st.info("Technical indicators coming soon")

with menu[10]:
    st.info("Pivot scanner coming soon")
