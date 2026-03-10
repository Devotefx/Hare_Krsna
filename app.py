import streamlit as st
import yfinance as yf
from binance.client import Client

st.title("Live Market Scanner")

# STOCK DATA
stock = yf.Ticker("AAPL")
data = stock.history(period="1d")

st.subheader("Stock Price (AAPL)")
st.line_chart(data["Close"])

# CRYPTO DATA
client = Client()

price = client.get_symbol_ticker(symbol="BTCUSDT")

st.subheader("BTC Price")
st.write(price)
