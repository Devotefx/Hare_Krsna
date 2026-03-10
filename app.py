import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Hare_Krsna", layout="wide")

st.title("📊 Live Market Scanner")

# -------- SETTINGS --------

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

breakouts = []
volume_spikes = []
big_money = []

# -------- DATA CACHE --------

@st.cache_data(ttl=300)
def get_data(symbol):
    return yf.download(symbol, period="5d", interval="15m")

# -------- SCAN --------

for s in stocks:

    try:

        data = get_data(s)

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

        if trade_value > 50000000:
            big_money.append(s)

        time.sleep(1)

    except:
        st.write(f"Error fetching {s}")

# -------- TRADINGVIEW LINK --------

def tv_link(symbol):
    sym = symbol.replace(".NS","")
    url = f"https://www.tradingview.com/chart/?symbol=NSE:{sym}"
    return f'<a href="{url}" target="_blank">{sym}</a>'

# -------- BUILD TABLE --------

results = []

for s in breakouts:
    results.append({"Symbol": tv_link(s), "Signal": "🚀 Breakout"})

for s in volume_spikes:
    results.append({"Symbol": tv_link(s), "Signal": "🔥 Volume Spike"})

for s in big_money:
    results.append({"Symbol": tv_link(s), "Signal": "💰 Big Money"})

df = pd.DataFrame(results)

# -------- DISPLAY --------

st.subheader("Scanner Results")

if len(df) > 0:

    st.markdown(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

else:

    st.write("No signals detected.")
