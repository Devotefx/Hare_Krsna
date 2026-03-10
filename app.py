import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="DevoteFX Scanner", layout="wide")

st.title("📊 Live Market Scanner")

# -------- STOCK LIST --------

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

# -------- DOWNLOAD ALL DATA AT ONCE --------

@st.cache_data(ttl=300)
def load_data():

    data = yf.download(
        tickers=stocks,
        period="5d",
        interval="15m",
        group_by="ticker",
        progress=False
    )

    return data

data = load_data()

breakouts = []
volume_spikes = []
big_money = []

# -------- SCAN --------

for s in stocks:

    try:

        df = data[s]

        if len(df) < 20:
            continue

        price = df["Close"].iloc[-1]
        high20 = df["High"].rolling(20).max().iloc[-2]

        volume = df["Volume"].iloc[-1]
        avg_volume = df["Volume"].rolling(20).mean().iloc[-2]

        trade_value = price * volume

        if price > high20:
            breakouts.append(s)

        if volume > 3 * avg_volume:
            volume_spikes.append(s)

        if trade_value > 50000000:
            big_money.append(s)

    except:
        st.write(f"Data unavailable for {s}")

# -------- TRADINGVIEW LINK --------

def tv_link(symbol):

    clean = symbol.replace(".NS","")

    url = f"https://www.tradingview.com/chart/?symbol=NSE:{clean}"

    return f'<a href="{url}" target="_blank">{clean}</a>'

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
