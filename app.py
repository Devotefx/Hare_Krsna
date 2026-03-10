import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="DevoteFX PRO", layout="wide", page_icon="📊")
st.title("📊 DevoteFX PRO Market Scanner")

# -------- STOCK LISTS --------

NIFTY50 = [
    "RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","HINDUNILVR","SBIN","LT",
    "BHARTIARTL","KOTAKBANK","AXISBANK","ITC","WIPRO","HCLTECH","ASIANPAINT",
    "MARUTI","SUNPHARMA","TITAN","ULTRACEMCO","BAJFINANCE","NESTLEIND","POWERGRID",
    "NTPC","TECHM","INDUSINDBK","BAJAJFINSV","ONGC","TATAMOTORS","TATASTEEL",
    "JSWSTEEL","COALINDIA","BPCL","GRASIM","ADANIPORTS","DIVISLAB","DRREDDY",
    "CIPLA","EICHERMOT","HEROMOTOCO","M&M","BRITANNIA","SHREECEM","UPL","APOLLOHOSP",
    "TATACONSUM","HINDALCO","VEDL","SBILIFE","HDFCLIFE","LTI"
]

NIFTY_FNO = [
    "RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","HINDUNILVR","SBIN","LT",
    "BHARTIARTL","KOTAKBANK","AXISBANK","ITC","WIPRO","HCLTECH","ASIANPAINT",
    "MARUTI","SUNPHARMA","TITAN","ULTRACEMCO","BAJFINANCE","NESTLEIND","POWERGRID",
    "NTPC","TECHM","INDUSINDBK","BAJAJFINSV","ONGC","TATAMOTORS","TATASTEEL",
    "JSWSTEEL","COALINDIA","BPCL","GRASIM","ADANIPORTS","DIVISLAB","DRREDDY",
    "CIPLA","EICHERMOT","HEROMOTOCO","M&M","BRITANNIA","SHREECEM","UPL","APOLLOHOSP",
    "TATACONSUM","HINDALCO","VEDL","SBILIFE","HDFCLIFE","LTI","MCDOWELL-N",
    "BIOCON","BANKBARODA","CANBK","PNB","FEDERALBNK","IDFCFIRSTB","RBLBANK",
    "BANDHANBNK","AUBANK","CHOLAFIN","MUTHOOTFIN","L&TFH","PFC","RECLTD","IRFC",
    "ADANIENT","ADANIGREEN","ADANITRANS","ADANIPORTS","DMART","NAUKRI","ZOMATO",
    "PAYTM","POLICYBZR","IRCTC","HAL","BEL","BHEL","SIEMENS","ABB","HAVELLS",
    "VOLTAS","WHIRLPOOL","CROMPTON","POLYCAB","KEI","APLAPOLLO","SAIL","NMDC",
    "MOIL","NATIONALUM","HINDCOPPER","GMRINFRA","GODREJPROP","OBEROIRLTY",
    "PHOENIXLTD","PRESTIGE","BRIGADE","DLF","SOBHA","MAHLIFE","SUNTV","ZEEL",
    "PVRINOX","INOXWIND","TATAPOWER","CESC","TORNTPOWER","NLCINDIA","SJVN",
    "NPCIL","IPCALAB","LUPIN","AUROPHARMA","TORNTPHARM","ALKEM","GLENMARK",
    "LALPATHLAB","METROPOLIS","THYROCARE","MAXHEALTH","FORTIS","STAR","ICICIGI",
    "HDFCAMC","NIPPONFIN","MIDHANI","MAZAGON","COCHINSHIP","GRSE","BEML","BDL",
    "TATACHEM","PIDILITIND","ASTRAL","AAPL","BALRAMCHIN","RENUKA","TRIVENI",
    "CHAMBLFERT","GNFC","GSFC","COROMANDEL","RALLIS","PI","BAYER","DEEPAKFERT",
    "DEEPAKNTR","ATUL","AARTIIND","VINATI","CLEAN","SUDARSCHEM","FINEORG",
    "IDFCFIRSTB","EQUITASBNK","UJJIVANSFB","ESAFSFB","CAPF","LICHSGFIN",
    "CANFINHOME","GRUH","REPCO","AAVAS","HOMEFIRST","PNBHOUSING","INDIABULL",
    "MANAPPURAM","BAJAJHLDNG","MOTILALOFS","IIFL","5PAISA","ANAND","EMAMILTD",
    "DABUR","MARICO","GODREJCP","JYOTHYLAB","COLPAL","GILLETTE","VGURD",
    "BATAINDIA","RAYMOND","PAGEIND","CENTURY","SIYARAM","GOKEX","RUPA",
    "TRENT","SHOPERSTOP","VMART","VSFPROJECTS","TASTYBITE"
]

BSE_ALL = NIFTY_FNO + [
    "WIPRO","MPHASIS","PERSISTENT","COFORGE","LTTS","KPITTECH","TATAELXSI",
    "HEXAWARE","SONATSOFTW","MASTEK","NIITLTD","RATEGAIN","ROUTE","TANLA",
    "INTELLECT","NUCLEUS","NEWGEN","RPGLIFE","EIDPARRY","HSCL","SPENCERS",
    "BERGEPAINT","KANSAINER","AKZONOBEL","JKCEMENT","RAMCOCEM","HEIDELBERG",
    "BIRLACORPN","DALMIA","JKLAKSHMI","PRISM","ORIENTCEM","NUVOCO"
]

MARKET_MAP = {
    "Nifty 50": NIFTY50,
    "Nifty F&O (~180 stocks)": NIFTY_FNO,
    "BSE All (Extended)": BSE_ALL,
}

def get_tickers(symbols):
    return [s + ".NS" for s in symbols]

# -------- CACHE DATA --------
@st.cache_data(ttl=300, show_spinner="📡 Fetching market data...")
def load_data(symbols):
    tickers = get_tickers(symbols)
    raw = yf.download(
        tickers=tickers,
        period="10d",
        interval="15m",
        group_by="ticker",
        progress=False,
        threads=True
    )
    return raw

def safe_get(data, symbol, col):
    try:
        ticker = symbol + ".NS"
        if ticker in data.columns.get_level_values(0):
            return data[ticker][col]
        elif col in data.columns:
            return data[col]
        return pd.Series(dtype=float)
    except:
        return pd.Series(dtype=float)

def analyze_stocks(data, symbols, min_cr):
    big_money, breakout, volume_spike, trap, liquidity = [], [], [], [], []
    order_blocks, smart_money, accumulation, technical, pivot_data = [], [], [], [], []

    for s in symbols:
        try:
            df = safe_get(data, s, "Close").to_frame("Close")
            df["High"]   = safe_get(data, s, "High")
            df["Low"]    = safe_get(data, s, "Low")
            df["Open"]   = safe_get(data, s, "Open")
            df["Volume"] = safe_get(data, s, "Volume")
            df.dropna(inplace=True)
            if len(df) < 25:
                continue

            price      = float(df["Close"].iloc[-1])
            vol        = float(df["Volume"].iloc[-1])
            avg_vol    = float(df["Volume"].rolling(20).mean().iloc[-2])
            trade_val  = price * vol / 1e7
            high20     = float(df["High"].rolling(20).max().iloc[-2])
            low20      = float(df["Low"].rolling(20).min().iloc[-2])
            open_price = float(df["Open"].iloc[-1])

            # Big Money
            if trade_val > min_cr:
                big_money.append([s, round(price, 2), round(trade_val, 2), "🟢" if price > open_price else "🔴"])

            # Breakout
            if price > high20:
                pct = round((price - high20) / high20 * 100, 2)
                breakout.append([s, round(price, 2), round(high20, 2), f"+{pct}%"])

            # Volume Spike
            if avg_vol > 0 and vol > 2.5 * avg_vol:
                ratio = round(vol / avg_vol, 1)
                volume_spike.append([s, round(price, 2), int(vol), f"{ratio}x"])

            # Trap Detection (bull/bear traps)
            prev_high = float(df["High"].iloc[-2])
            prev_low  = float(df["Low"].iloc[-2])
            curr_close = float(df["Close"].iloc[-1])
            curr_open  = float(df["Open"].iloc[-1])
            if curr_close < curr_open and df["High"].iloc[-1] > prev_high:
                trap.append([s, round(price, 2), "🐻 Bear Trap (False Breakout Up)"])
            elif curr_close > curr_open and df["Low"].iloc[-1] < prev_low:
                trap.append([s, round(price, 2), "🐂 Bull Trap (False Breakout Down)"])

            # Liquidity Zones
            swing_high = float(df["High"].rolling(10).max().iloc[-1])
            swing_low  = float(df["Low"].rolling(10).min().iloc[-1])
            if abs(price - swing_high) / swing_high < 0.005:
                liquidity.append([s, round(price, 2), round(swing_high, 2), "Near Resistance Liquidity"])
            elif abs(price - swing_low) / swing_low < 0.005:
                liquidity.append([s, round(price, 2), round(swing_low, 2), "Near Support Liquidity"])

            # Order Blocks
            body = abs(df["Close"].iloc[-3] - df["Open"].iloc[-3])
            candle_range = df["High"].iloc[-3] - df["Low"].iloc[-3]
            if candle_range > 0 and body / candle_range > 0.7:
                direction = "Bullish OB" if df["Close"].iloc[-3] > df["Open"].iloc[-3] else "Bearish OB"
                order_blocks.append([s, round(price, 2), round(df["Open"].iloc[-3], 2), round(df["Close"].iloc[-3], 2), direction])

            # Smart Money (large candles with high volume)
            candle_size = abs(df["Close"].iloc[-1] - df["Open"].iloc[-1])
            avg_candle  = (df["Close"] - df["Open"]).abs().rolling(20).mean().iloc[-2]
            if candle_size > 2 * avg_candle and vol > 1.5 * avg_vol:
                direction = "Bullish Impulse" if curr_close > curr_open else "Bearish Impulse"
                smart_money.append([s, round(price, 2), round(candle_size, 2), direction])

            # Accumulation (sideways price, rising volume)
            price_range = (df["Close"].rolling(10).max() - df["Close"].rolling(10).min()).iloc[-1]
            price_mean  = df["Close"].rolling(10).mean().iloc[-1]
            if price_mean > 0 and price_range / price_mean < 0.03 and vol > avg_vol:
                accumulation.append([s, round(price, 2), round(price_range / price_mean * 100, 2)])

            # Technical Indicators
            ema9  = float(df["Close"].ewm(span=9).mean().iloc[-1])
            ema21 = float(df["Close"].ewm(span=21).mean().iloc[-1])
            delta = df["Close"].diff()
            gain  = delta.clip(lower=0).rolling(14).mean()
            loss  = (-delta.clip(upper=0)).rolling(14).mean()
            rs    = gain / loss.replace(0, np.nan)
            rsi   = float((100 - 100 / (1 + rs)).iloc[-1])
            signal = "BUY" if (ema9 > ema21 and rsi < 70) else ("SELL" if ema9 < ema21 and rsi > 30 else "HOLD")
            technical.append([s, round(price, 2), round(ema9, 2), round(ema21, 2), round(rsi, 1), signal])

            # Pivot Points
            ph = float(df["High"].iloc[-2])
            pl = float(df["Low"].iloc[-2])
            pc = float(df["Close"].iloc[-2])
            pp = round((ph + pl + pc) / 3, 2)
            r1 = round(2 * pp - pl, 2)
            s1 = round(2 * pp - ph, 2)
            r2 = round(pp + (ph - pl), 2)
            s2 = round(pp - (ph - pl), 2)
            near = "Above PP" if price > pp else "Below PP"
            pivot_data.append([s, round(price, 2), pp, s2, s1, r1, r2, near])

        except Exception as e:
            continue

    return big_money, breakout, volume_spike, trap, liquidity, order_blocks, smart_money, accumulation, technical, pivot_data

# -------- CONTROLS --------
st.markdown("---")
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    market = st.selectbox("🌐 Market", list(MARKET_MAP.keys()))
with col2:
    min_cr = st.number_input("Min ₹Cr", value=4, min_value=0)
with col3:
    run = st.button("▶ RUN SCAN", use_container_width=True)
with col4:
    auto = st.checkbox("⏱ Auto")

st.markdown("---")

# -------- TABS --------
menu = st.tabs([
    "💰 Big Money", "🌡️ Heatmap", "🪤 Trap", "💧 Liquidity",
    "📦 Order Block", "💎 Smart Money", "📥 Accumulation",
    "📊 Volume", "📈 Technical", "🚀 Breakout", "🎯 Pivot"
])

if run or auto:
    symbols = MARKET_MAP[market]
    with st.spinner(f"Scanning {len(symbols)} stocks..."):
        data = load_data(symbols)
        (big_money, breakout, volume_spike, trap, liquidity,
         order_blocks, smart_money, accumulation, technical, pivot_data) = analyze_stocks(data, symbols, min_cr)

    # TAB 0 - Big Money
    with menu[0]:
        st.subheader("💰 Big Money Flow")
        if big_money:
            df = pd.DataFrame(big_money, columns=["Symbol", "Price (₹)", "Trade Value (₹Cr)", "Trend"])
            df = df.sort_values("Trade Value (₹Cr)", ascending=False).reset_index(drop=True)
            st.success(f"Found {len(df)} stocks with big money flow (>{min_cr} Cr)")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No big money stocks found. Try lowering Min ₹Cr.")

    # TAB 1 - Heatmap
    with menu[1]:
        st.subheader("🌡️ Market Heatmap")
        if technical:
            df = pd.DataFrame(technical, columns=["Symbol", "Price", "EMA9", "EMA21", "RSI", "Signal"])
            df["Color"] = df["Signal"].map({"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡"})
            buy   = df[df["Signal"] == "BUY"]
            sell  = df[df["Signal"] == "SELL"]
            hold  = df[df["Signal"] == "HOLD"]
            c1, c2, c3 = st.columns(3)
            c1.metric("🟢 Bullish", len(buy))
            c2.metric("🔴 Bearish", len(sell))
            c3.metric("🟡 Neutral", len(hold))
            st.markdown("**Signal Distribution**")
            st.dataframe(df[["Symbol","Price","RSI","Signal","Color"]].sort_values("RSI"), use_container_width=True)
        else:
            st.warning("Run scan to see heatmap.")

    # TAB 2 - Trap
    with menu[2]:
        st.subheader("🪤 Trap Detection (Bull/Bear Traps)")
        if trap:
            df = pd.DataFrame(trap, columns=["Symbol", "Price (₹)", "Trap Type"])
            st.warning(f"⚠️ {len(df)} potential trap(s) detected!")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No traps detected in current scan.")

    # TAB 3 - Liquidity
    with menu[3]:
        st.subheader("💧 Liquidity Zones")
        if liquidity:
            df = pd.DataFrame(liquidity, columns=["Symbol", "Price (₹)", "Zone Level (₹)", "Zone Type"])
            st.success(f"{len(df)} stocks near key liquidity zones")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No liquidity zone touches detected.")

    # TAB 4 - Order Block
    with menu[4]:
        st.subheader("📦 Order Block Detection")
        if order_blocks:
            df = pd.DataFrame(order_blocks, columns=["Symbol", "Price (₹)", "OB Open", "OB Close", "Type"])
            st.success(f"{len(df)} order blocks identified")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No clear order blocks found.")

    # TAB 5 - Smart Money
    with menu[5]:
        st.subheader("💎 Smart Money Moves")
        if smart_money:
            df = pd.DataFrame(smart_money, columns=["Symbol", "Price (₹)", "Candle Size", "Direction"])
            df = df.sort_values("Candle Size", ascending=False).reset_index(drop=True)
            st.success(f"{len(df)} smart money impulses detected")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No smart money moves detected.")

    # TAB 6 - Accumulation
    with menu[6]:
        st.subheader("📥 Accumulation Zones")
        if accumulation:
            df = pd.DataFrame(accumulation, columns=["Symbol", "Price (₹)", "Price Range %"])
            df = df.sort_values("Price Range %").reset_index(drop=True)
            st.success(f"{len(df)} stocks in accumulation")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No accumulation zones found.")

    # TAB 7 - Volume
    with menu[7]:
        st.subheader("📊 Volume Spikes")
        if volume_spike:
            df = pd.DataFrame(volume_spike, columns=["Symbol", "Price (₹)", "Volume", "Ratio vs Avg"])
            df = df.sort_values("Volume", ascending=False).reset_index(drop=True)
            st.success(f"{len(df)} volume spikes detected (>2.5x average)")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No significant volume spikes found.")

    # TAB 8 - Technical
    with menu[8]:
        st.subheader("📈 Technical Indicators (EMA + RSI)")
        if technical:
            df = pd.DataFrame(technical, columns=["Symbol", "Price (₹)", "EMA9", "EMA21", "RSI", "Signal"])
            df = df.sort_values("RSI").reset_index(drop=True)
            st.dataframe(
                df.style.applymap(
                    lambda v: "background-color:#1a3a1a;color:lightgreen" if v == "BUY"
                    else ("background-color:#3a1a1a;color:#ff6b6b" if v == "SELL" else ""),
                    subset=["Signal"]
                ),
                use_container_width=True
            )
        else:
            st.warning("No technical data available.")

    # TAB 9 - Breakout
    with menu[9]:
        st.subheader("🚀 Breakouts (20-period High)")
        if breakout:
            df = pd.DataFrame(breakout, columns=["Symbol", "Price (₹)", "20H Level (₹)", "Breakout %"])
            df = df.sort_values("Breakout %", ascending=False).reset_index(drop=True)
            st.success(f"{len(df)} breakout(s) detected!")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No breakouts detected currently.")

    # TAB 10 - Pivot
    with menu[10]:
        st.subheader("🎯 Pivot Points (Classic)")
        if pivot_data:
            df = pd.DataFrame(pivot_data, columns=["Symbol", "Price (₹)", "PP", "S2", "S1", "R1", "R2", "Position"])
            st.success(f"Pivot levels for {len(df)} stocks")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No pivot data available.")

else:
    for i, tab in enumerate(menu):
        with tab:
            st.info("🔍 Select a market and press **▶ RUN SCAN** to begin analysis.")

# -------- FOOTER --------
st.markdown("---")
st.caption(
    "📡 DevoteFX PRO | Data: Yahoo Finance | Market hours: 9:15–15:30 IST (NSE/BSE) | "
    "Refresh interval: 5 min cache | ⚠️ For educational purposes only."
)
