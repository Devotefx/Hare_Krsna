from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import pandas as pd

app = FastAPI()

# -------- STOCK LIST --------

NIFTY50 = [
"RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
"HINDUNILVR.NS","SBIN.NS","LT.NS","AXISBANK.NS","KOTAKBANK.NS"
]

# -------- ROOT PAGE --------

@app.get("/")
def root():
    return FileResponse("index.html")

# -------- SCANNER --------

@app.get("/api/scan/{mode}")
def scan(mode: str, universe: str = "nifty50"):

    stocks = NIFTY50

    results = []

    for s in stocks:

        try:

            data = yf.download(
                s,
                period="5d",
                interval="15m",
                progress=False
            )

            if len(data) < 20:
                continue

            price = round(data["Close"].iloc[-1],2)

            volume = data["Volume"].iloc[-1]

            avg_vol = data["Volume"].rolling(20).mean().iloc[-2]

            trade_value = price * volume / 10000000

            signal = "Neutral"
            color = "green"

            if price > data["High"].rolling(20).max().iloc[-2]:
                signal = "Breakout"

            if volume > 3 * avg_vol:
                signal = "Volume Spike"

            if trade_value > 5:
                signal = "Big Money"

            results.append({

                "symbol": s.replace(".NS",""),
                "price": price,
                "trend": signal,
                "signal_color": "green",
                "value_cr": round(trade_value,2)

            })

        except:
            pass

    return {"results": results}
