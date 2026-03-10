import streamlit as st
import yfinance as yf
from binance.client import Client
import pandas as pd

st.title("📊 Swing Trading Market Scanner")

# ----------------------------
# SETTINGS
# ----------------------------

big_money_threshold = st.sidebar.number_input(
    "Big Money Threshold (₹ Crore)",
    min_value=1,
    max_value=100,
    value=5
)

big_money_value = big_money_threshold * 10000000

timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["15m", "1h"]
)

# ----------------------------
# STOCK LIST
# ----------------------------

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "AXISBANK.NS"
]

breakouts = []
volume_spikes = []
big_money = []

# ----------------------------
# SCANNER
# ----------------------------

for s in stocks:

    try:

        data = yf.download(
            s,
            period="5d",
            interval=timeframe
        )

        if len(data) < 20:
            continue

        price = data["Close"].iloc[-1]

        high20 = data["High"].rolling(20).max().iloc[-2]

        volume = data["Volume"].iloc[-1]

        avg_volume = data["Volume"].rolling(20).mean().iloc[-2]

        trade_value = price * volume

        if price > high20:
            breakouts.append(s)

        if volume > 3 * avg_volume:
            volume_spikes.append(s)

        if trade_value > big_money_value:
            big_money.append(s)

    except:
        pass

# ----------------------------
# RESULTS
# ----------------------------

st.header("🚀 Breakouts")

for s in breakouts:
    st.write(s)

st.header("🔥 Volume Spikes")

for s in volume_spikes:
    st.write(s)

st.header("💰 Big Money Trades")

for s in big_money:
    st.write(s)

# ----------------------------
# CRYPTO
# ----------------------------

st.header("₿ Crypto Market")

client = Client()

btc = client.get_symbol_ticker(symbol="BTCUSDT")
eth = client.get_symbol_ticker(symbol="ETHUSDT")

st.write("BTC Price:", btc["price"])
st.write("ETH Price:", eth["price"])
