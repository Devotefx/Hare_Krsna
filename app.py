import streamlit as st
import yfinance as yf
import time
import pandas as pd
import streamlit as st

def tradingview_link(symbol):
    clean_symbol = symbol.replace(".NS","")
    url = f"https://www.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank">{clean_symbol}</a>'
st.title("📊 Live Market Scanner")

# Cache data to avoid repeated Yahoo calls
@st.cache_data(ttl=300)
def get_stock_data(symbol):
    data = yf.download(symbol, period="5d", interval="15m")
    return data

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
]

breakouts = []
volume_spikes = []

for s in stocks:

    try:

        data = get_stock_data(s)

        if len(data) < 20:
            continue

        price = data["Close"].iloc[-1]
        high20 = data["High"].rolling(20).max().iloc[-2]

        volume = data["Volume"].iloc[-1]
        avg_volume = data["Volume"].rolling(20).mean().iloc[-2]

        if price > high20:
            breakouts.append(s)

        if volume > 3 * avg_volume:
            volume_spikes.append(s)

        time.sleep(1)   # prevents rate limit

    except Exception as e:
        st.write(f"Error fetching {s}")

import pandas as pd

def tradingview_link(symbol):
    clean_symbol = symbol.replace(".NS","")
    url = f"https://www.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
    return f'<a href="{url}" target="_blank">{clean_symbol}</a>'

results = []

for s in breakouts:
    results.append({
        "Symbol": tradingview_link(s),
        "Signal": "Breakout"
    })

for s in volume_spikes:
    results.append({
        "Symbol": tradingview_link(s),
        "Signal": "Volume Spike"
    })

for s in big_money:
    results.append({
        "Symbol": tradingview_link(s),
        "Signal": "Big Money"
    })

df = pd.DataFrame(results)

st.markdown(
    df.to_html(escape=False, index=False),
    unsafe_allow_html=True
)

