import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="DevoteFX PRO", layout="wide", page_icon="📊")
st.title("📊 DevoteFX PRO Market Scanner")

# ═══════════════════════════════════════════════════════
# STOCK LISTS
# ═══════════════════════════════════════════════════════
NIFTY50 = [
    "RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","HINDUNILVR","SBIN","LT",
    "BHARTIARTL","KOTAKBANK","AXISBANK","ITC","WIPRO","HCLTECH","ASIANPAINT",
    "MARUTI","SUNPHARMA","TITAN","ULTRACEMCO","BAJFINANCE","NESTLEIND","POWERGRID",
    "NTPC","TECHM","INDUSINDBK","BAJAJFINSV","ONGC","TATAMOTORS","TATASTEEL",
    "JSWSTEEL","COALINDIA","BPCL","GRASIM","ADANIPORTS","DIVISLAB","DRREDDY",
    "CIPLA","EICHERMOT","HEROMOTOCO","M&M","BRITANNIA","SHREECEM","UPL","APOLLOHOSP",
    "TATACONSUM","HINDALCO","VEDL","SBILIFE","HDFCLIFE","LTI"
]

SENSEX30 = [
    "RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","HINDUNILVR","ITC","SBIN",
    "BHARTIARTL","KOTAKBANK","AXISBANK","LT","BAJFINANCE","MARUTI","TITAN",
    "SUNPHARMA","ULTRACEMCO","ASIANPAINT","HCLTECH","WIPRO","NESTLEIND","M&M",
    "POWERGRID","NTPC","INDUSINDBK","TATAMOTORS","TATASTEEL","BAJAJFINSV",
    "ONGC","DRREDDY"
]

NIFTY_FNO = [
"RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","HINDUNILVR","SBIN","LT",
"BHARTIARTL","KOTAKBANK","AXISBANK","ITC","WIPRO","HCLTECH","ASIANPAINT",
"MARUTI","SUNPHARMA","TITAN","ULTRACEMCO","BAJFINANCE","NESTLEIND","POWERGRID",
"NTPC","TECHM","INDUSINDBK","BAJAJFINSV","ONGC","TATAMOTORS","TATASTEEL",
"JSWSTEEL","COALINDIA","BPCL","GRASIM","ADANIPORTS","DIVISLAB","DRREDDY",
"CIPLA","EICHERMOT","HEROMOTOCO","M&M","BRITANNIA","SHREECEM","UPL","APOLLOHOSP",
"TATACONSUM","HINDALCO","VEDL","SBILIFE","HDFCLIFE","LTIM","MCDOWELL-N",
"BIOCON","BANKBARODA","CANBK","PNB","FEDERALBNK","IDFCFIRSTB","RBLBANK",
"BANDHANBNK","AUBANK","CHOLAFIN","MUTHOOTFIN","PFC","RECLTD","IRFC",
"ADANIENT","ADANIGREEN","DMART","NAUKRI","ZOMATO","IRCTC","HAL","BEL",
"BHEL","SIEMENS","HAVELLS","POLYCAB","SAIL","NMDC","DLF","TATAPOWER",

"ABB","ABBOTINDIA","ACC","ADANITRANS","ALKEM","AMBUJACEM","APLLTD",
"ASHOKLEY","ASTRAL","ATUL","AUROPHARMA","BALKRISIND","BALRAMCHIN",
"BATAINDIA","BERGEPAINT","BHARATFORG","BOSCHLTD","CADILAHC","CANFINHOME",
"CASTROLIND","CEATLTD","CENTURYTEX","CESC","CHAMBLFERT","COLPAL",
"CONCOR","COROMANDEL","CROMPTON","CUB","DALBHARAT","DEEPAKNTR",
"DELHIVERY","DIXON","ESCORTS","EXIDEIND","GAIL","GLENMARK",
"GMRINFRA","GODREJCP","GODREJPROP","GRANULES","GUJGASLTD","HDFCAMC",
"HINDCOPPER","ICICIGI","ICICIPRULI","IDEA","IGL","INDHOTEL",
"INDIGO","INDUSTOWER","IPCALAB","JINDALSTEL","JKCEMENT","JSWENERGY",
"JUBLFOOD","KALPATPOWR","KEC","LALPATHLAB","LAURUSLABS","LICHSGFIN",
"LINDEINDIA","LUPIN","MGL","MPHASIS","MRF","NATIONALUM",
"OBEROIRLTY","OFSS","PAGEIND","PEL","PERSISTENT","PETRONET",
"PIIND","PNBHOUSING","RAMCOCEM","RATNAMANI","SAFARI","SANOFI",
"SRF","STAR","SUNTV","SYNGENE","TATACHEM","TATACOMM",
"TATELXSI","TORNTPHARM","TORNTPOWER","TRENT","TVSMOTOR",
"UBL","UNIONBANK","VOLTAS","WHIRLPOOL","ZYDUSLIFE"
]

BSE_ALL = list(dict.fromkeys(NIFTY_FNO + [
    "MPHASIS","PERSISTENT","COFORGE","LTTS","KPITTECH","TATAELXSI",
    "BERGEPAINT","KANSAINER","JKCEMENT","RAMCOCEM","DALMIA",
    "PIDILITIND","ASTRAL","TATACHEM","DABUR","MARICO","GODREJCP",
    "EMAMILTD","COLPAL","BATAINDIA","TRENT","PAGEIND","RAYMOND",
    "LUPIN","AUROPHARMA","TORNTPHARM","ALKEM","GLENMARK",
    "LALPATHLAB","GODREJPROP","OBEROIRLTY","PHOENIXLTD","PRESTIGE","BRIGADE"
]))

MCX_METALS   = {"GOLD":"GC=F","SILVER":"SI=F","COPPER":"HG=F","ALUMINIUM":"ALI=F","ZINC":"ZNC=F","NICKEL":"NI=F"}
MCX_ENERGY   = {"CRUDEOIL":"CL=F","NATURALGAS":"NG=F"}
MCX_ALL_COMM = {**MCX_METALS, **MCX_ENERGY, "COTTON":"CT=F"}
MCX_TICKER_MAP = {**MCX_ALL_COMM}

MARKET_MAP = {
    "Nifty 50":           (NIFTY50,                        "NSE"),
    "All F&O (74)":       (NIFTY_FNO,                     "NSE"),
    "Sensex 30":          (SENSEX30,                       "NSE"),
    "MCX Metals":         (list(MCX_METALS.keys()),        "MCX"),
    "MCX Energy":         (list(MCX_ENERGY.keys()),        "MCX"),
    "MCX All Comm":       (list(MCX_ALL_COMM.keys()),      "MCX"),
    "BSE All (Extended)": (BSE_ALL,                        "NSE"),
}

TF_MAP = {"5m":"5m", "15m":"15m", "Daily":"1d", "Weekly":"1wk"}

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def get_tickers(symbols, exchange):
    if exchange == "MCX":
        return [MCX_TICKER_MAP.get(s, s) for s in symbols]
    return [s + ".NS" for s in symbols]

@st.cache_data(ttl=300, show_spinner="📡 Fetching market data...")
def load_data(symbols_tuple, interval, exchange):
    symbols = list(symbols_tuple)
    tickers = get_tickers(symbols, exchange)
    period  = "60d" if interval in ("1d","1wk") else "10d"
    return yf.download(tickers=tickers, period=period, interval=interval,
                       group_by="ticker", progress=False, threads=True)

def safe_get(data, symbol, exchange, col):
    try:
        ticker = MCX_TICKER_MAP.get(symbol, symbol+".NS") if exchange=="MCX" else symbol+".NS"
        lvl0 = data.columns.get_level_values(0)
        if ticker in lvl0:
            return data[ticker][col]
        elif col in data.columns:
            return data[col]
        return pd.Series(dtype=float)
    except:
        return pd.Series(dtype=float)

def vol_label(vol):
    if vol >= 1e7:  return f"{vol/1e7:.2f} Cr"
    elif vol >= 1e5: return f"{vol/1e5:.2f} L"
    else:            return f"{int(vol):,}"

# ═══════════════════════════════════════════════════════
# ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════
def analyze_stocks(data, symbols, exchange, min_cr):
    big_money, breakout, volume_spike, trap, liquidity = [], [], [], [], []
    order_blocks, smart_money, accumulation, technical, pivot_data = [], [], [], [], []

    for s in symbols:
        try:
            df = safe_get(data, s, exchange, "Close").to_frame("Close")
            df["High"]   = safe_get(data, s, exchange, "High")
            df["Low"]    = safe_get(data, s, exchange, "Low")
            df["Open"]   = safe_get(data, s, exchange, "Open")
            df["Volume"] = safe_get(data, s, exchange, "Volume")
            df.dropna(inplace=True)
            if len(df) < 25: continue

            price      = float(df["Close"].iloc[-1])
            vol        = float(df["Volume"].iloc[-1])
            avg_vol    = float(df["Volume"].rolling(20).mean().iloc[-2])
            trade_val  = price * vol / 1e7
            high20     = float(df["High"].rolling(20).max().iloc[-2])
            open_price = float(df["Open"].iloc[-1])
            curr_close = price; curr_open = open_price

            if trade_val > min_cr:
                big_money.append([s, round(price,2), round(trade_val,2), "🟢" if price>open_price else "🔴"])
            if price > high20:
                pct = round((price-high20)/high20*100,2)
                breakout.append([s, round(price,2), round(high20,2), f"+{pct}%"])
            if avg_vol > 0 and vol > 2.5*avg_vol:
                volume_spike.append([s, round(price,2), int(vol), f"{round(vol/avg_vol,1)}x"])

            prev_high = float(df["High"].iloc[-2]); prev_low = float(df["Low"].iloc[-2])
            if curr_close < curr_open and df["High"].iloc[-1] > prev_high:
                trap.append([s, round(price,2), "🐻 Bear Trap"])
            elif curr_close > curr_open and df["Low"].iloc[-1] < prev_low:
                trap.append([s, round(price,2), "🐂 Bull Trap"])

            swing_high = float(df["High"].rolling(10).max().iloc[-1])
            swing_low  = float(df["Low"].rolling(10).min().iloc[-1])
            if abs(price-swing_high)/swing_high < 0.005:
                liquidity.append([s, round(price,2), round(swing_high,2), "Near Resistance"])
            elif abs(price-swing_low)/swing_low < 0.005:
                liquidity.append([s, round(price,2), round(swing_low,2), "Near Support"])

            body = abs(df["Close"].iloc[-3]-df["Open"].iloc[-3])
            cr   = df["High"].iloc[-3]-df["Low"].iloc[-3]
            if cr > 0 and body/cr > 0.7:
                order_blocks.append([s, round(price,2), round(df["Open"].iloc[-3],2),
                    round(df["Close"].iloc[-3],2),
                    "Bullish OB" if df["Close"].iloc[-3]>df["Open"].iloc[-3] else "Bearish OB"])

            candle_size = abs(df["Close"].iloc[-1]-df["Open"].iloc[-1])
            avg_candle  = (df["Close"]-df["Open"]).abs().rolling(20).mean().iloc[-2]
            if candle_size > 2*avg_candle and avg_vol>0 and vol > 1.5*avg_vol:
                smart_money.append([s, round(price,2), round(candle_size,2),
                    "Bullish Impulse" if curr_close>curr_open else "Bearish Impulse"])

            price_range = (df["Close"].rolling(10).max()-df["Close"].rolling(10).min()).iloc[-1]
            price_mean  = df["Close"].rolling(10).mean().iloc[-1]
            if price_mean>0 and price_range/price_mean<0.03 and avg_vol>0 and vol>avg_vol:
                accumulation.append([s, round(price,2), round(price_range/price_mean*100,2)])

            ema9  = float(df["Close"].ewm(span=9).mean().iloc[-1])
            ema21 = float(df["Close"].ewm(span=21).mean().iloc[-1])
            delta = df["Close"].diff()
            gain  = delta.clip(lower=0).rolling(14).mean()
            loss  = (-delta.clip(upper=0)).rolling(14).mean()
            rs    = gain / loss.replace(0, np.nan)
            rsi   = float((100-100/(1+rs)).iloc[-1])
            signal = "BUY" if (ema9>ema21 and rsi<70) else ("SELL" if ema9<ema21 and rsi>30 else "HOLD")
            technical.append([s, round(price,2), round(ema9,2), round(ema21,2), round(rsi,1), signal])

            ph=float(df["High"].iloc[-2]); pl=float(df["Low"].iloc[-2]); pc=float(df["Close"].iloc[-2])
            pp=round((ph+pl+pc)/3,2)
            pivot_data.append([s, round(price,2), pp,
                round(pp-(ph-pl),2), round(2*pp-ph,2), round(2*pp-pl,2), round(pp+(ph-pl),2),
                "Above PP" if price>pp else "Below PP"])
        except:
            continue

    return big_money, breakout, volume_spike, trap, liquidity, order_blocks, smart_money, accumulation, technical, pivot_data

def scan_volume_tab(symbols, exchange, interval, min_mult):
    try:
        raw = load_data(tuple(symbols), interval, exchange)
    except:
        return []
    results = []
    for s in symbols:
        try:
            close_s = safe_get(raw, s, exchange, "Close").dropna()
            vol_s   = safe_get(raw, s, exchange, "Volume").dropna()
            open_s  = safe_get(raw, s, exchange, "Open").dropna()
            if len(close_s) < 22 or len(vol_s) < 22: continue
            price   = float(close_s.iloc[-1])
            vol     = float(vol_s.iloc[-1])
            avg_vol = float(vol_s.rolling(20).mean().iloc[-2])
            if avg_vol <= 0: continue
            ratio   = vol / avg_vol
            if ratio < min_mult: continue
            prev_close = float(close_s.iloc[-2])
            pct_chg    = (price - prev_close) / prev_close * 100
            curr_open  = float(open_s.iloc[-1]) if len(open_s) > 0 else price
            bullish    = price >= curr_open
            if bullish:
                spike_type,signal_lbl = "🟢 BULL SPIKE","🟢 Buying"
                card_color,border_col,txt_col = "#0d3320","#00e676","#69f0ae"
            else:
                spike_type,signal_lbl = "🔴 BEAR SPIKE","🔴 Selling"
                card_color,border_col,txt_col = "#3a0808","#ff1744","#ff6b6b"
            results.append(dict(
                symbol=s, exchange=exchange, price=price, pct_chg=pct_chg,
                vol=vol, avg_vol=avg_vol, ratio=ratio, bullish=bullish,
                spike_type=spike_type, signal_lbl=signal_lbl,
                card_color=card_color, border_col=border_col, txt_col=txt_col,
                interval=interval
            ))
        except:
            continue
    results.sort(key=lambda x: x["ratio"], reverse=True)
    return results

# ═══════════════════════════════════════════════════════
# GLOBAL CONTROLS
# ═══════════════════════════════════════════════════════
st.markdown("---")
gc1, gc2, gc3, gc4 = st.columns([2,1,1,1])
with gc1:
    market_name = st.selectbox("🌐 Market", list(MARKET_MAP.keys()))
with gc2:
    min_cr = st.number_input("Min ₹Cr", value=4, min_value=0)
with gc3:
    run = st.button("▶ RUN SCAN", use_container_width=True)
with gc4:
    auto = st.checkbox("⏱ Auto")
st.markdown("---")

symbols, exchange = MARKET_MAP[market_name]

# ═══════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════
menu = st.tabs([
    "💰 Big Money","🌡️ Heatmap","🪤 Trap","💧 Liquidity",
    "📦 Order Block","💎 Smart Money","📥 Accumulation",
    "📊 Volume","📈 Technical","🚀 Breakout","🎯 Pivot"
])

# ─── TAB 7: VOLUME (own controls) ───────────────────────────────────
with menu[7]:
    st.subheader("📊 Volume Spike Scanner")

    vc1,vc2,vc3,vc4,vc5 = st.columns([2,1,1,1,1])
    with vc1:
        vol_market = st.selectbox("Market", list(MARKET_MAP.keys()), key="vol_market")
    with vc2:
        vol_tf_label = st.selectbox("TF", list(TF_MAP.keys()), index=1, key="vol_tf")
        vol_interval = TF_MAP[vol_tf_label]
    with vc3:
        preset_mult = st.selectbox("Min×", ["2x","3x","Custom"], index=0, key="vol_preset")
    with vc4:
        if preset_mult == "Custom":
            min_mult = st.number_input("Custom ×", min_value=1.0, max_value=20.0, value=2.0, step=0.5, key="vol_custom")
        else:
            min_mult = float(preset_mult.replace("x",""))
            st.metric("Multiplier", f"{min_mult}×")
    with vc5:
        vol_run = st.button("▶ SCAN VOLUME", use_container_width=True, key="vol_run")

    vol_syms, vol_exch = MARKET_MAP[vol_market]

    if vol_run or auto:
        with st.spinner(f"Scanning {len(vol_syms)} stocks ≥ {min_mult}× on {vol_tf_label}…"):
            vol_results = scan_volume_tab(vol_syms, vol_exch, vol_interval, min_mult)

        total = len(vol_syms); found = len(vol_results)
        bulls = sum(1 for r in vol_results if r["bullish"]); bears = found - bulls
        sm1,sm2,sm3,sm4 = st.columns(4)
        sm1.metric("Found", f"{found} / {total}")
        sm2.metric("🟢 Bull Spikes", bulls)
        sm3.metric("🔴 Bear Spikes", bears)
        sm4.metric("Threshold", f"{min_mult}×")

        if vol_results:
            cards_html = """
            <style>
            .vol-grid{display:flex;flex-wrap:wrap;gap:10px;padding:14px 0}
            .vol-card{width:195px;border-radius:10px;padding:12px 14px;
                font-family:'Segoe UI',sans-serif;border-left:4px solid;
                box-shadow:0 2px 8px rgba(0,0,0,.5)}
            .vc-sym {font-size:15px;font-weight:800;letter-spacing:.5px}
            .vc-exch{font-size:10px;opacity:.6;margin-bottom:3px}
            .vc-price{font-size:14px;font-weight:600}
            .vc-sig {font-size:11px;margin:3px 0}
            .vc-spike{font-size:12px;font-weight:700;margin:2px 0}
            .vc-row {display:flex;justify-content:space-between;font-size:11px;margin-top:5px;opacity:.85}
            .vc-tf  {display:inline-block;background:rgba(255,255,255,.12);
                     border-radius:4px;padding:1px 7px;font-size:10px;margin-top:6px}
            </style>
            <div class="vol-grid">"""

            for r in vol_results:
                sign    = "+" if r["pct_chg"] >= 0 else ""
                pct_col = "#69f0ae" if r["pct_chg"] >= 0 else "#ff6b6b"
                cards_html += f"""
                <div class="vol-card" style="background:{r['card_color']};border-color:{r['border_col']};color:{r['txt_col']};">
                  <div class="vc-sym">{r['symbol']}</div>
                  <div class="vc-exch">{r['exchange']}</div>
                  <div class="vc-price">₹{r['price']:,.1f}&nbsp;
                    <span style="color:{pct_col}">{sign}{r['pct_chg']:.2f}%</span>
                  </div>
                  <div class="vc-sig">{r['signal_lbl']}</div>
                  <div class="vc-spike">{r['spike_type']}</div>
                  <div class="vc-row">
                    <span>{r['ratio']:.2f}× avg</span>
                    <span>{vol_label(r['vol'])}</span>
                  </div>
                  <div class="vc-tf">{r['interval']}</div>
                </div>"""
            cards_html += "</div>"
            st.markdown(cards_html, unsafe_allow_html=True)

            with st.expander("📋 Table View", expanded=False):
                df_vol = pd.DataFrame([{
                    "Symbol":r["symbol"],"Exchange":r["exchange"],
                    "Price (₹)":r["price"],"Change %":round(r["pct_chg"],2),
                    "Volume":vol_label(r["vol"]),"Avg Vol":vol_label(r["avg_vol"]),
                    "Ratio":round(r["ratio"],2),"Signal":r["spike_type"],"TF":r["interval"]
                } for r in vol_results])
                st.dataframe(df_vol, use_container_width=True)
        else:
            st.info(f"No spikes ≥ {min_mult}× found. Try lowering the multiplier or changing timeframe.")
    else:
        st.info("🔍 Configure above and press **▶ SCAN VOLUME**")

# ─── OTHER TABS ─────────────────────────────────────────────────────
if run or auto:
    with st.spinner(f"Scanning {len(symbols)} stocks…"):
        data = load_data(tuple(symbols), "15m", exchange)
        (big_money, breakout, volume_spike_g, trap, liquidity,
         order_blocks, smart_money, accumulation, technical, pivot_data) = analyze_stocks(data, symbols, exchange, min_cr)

    with menu[0]:
        st.subheader("💰 Big Money Flow")
        if big_money:
            df = pd.DataFrame(big_money, columns=["Symbol","Price (₹)","Trade Value (₹Cr)","Trend"])
            df = df.sort_values("Trade Value (₹Cr)", ascending=False).reset_index(drop=True)
            st.success(f"Found {len(df)} / {len(symbols)} stocks (>{min_cr} Cr)")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No big money stocks found. Try lowering Min ₹Cr.")

    with menu[1]:
        st.subheader("🌡️ Market Heatmap")
        heatmap_rows = []
        for s in symbols:
            try:
                closes = safe_get(data, s, exchange, "Close").dropna()
                if len(closes) < 2: continue
                price = float(closes.iloc[-1]); prev = float(closes.iloc[-2])
                heatmap_rows.append((s, price, (price-prev)/prev*100))
            except: continue
        heatmap_rows.sort(key=lambda x: x[2], reverse=True)

        def tile_color(pct):
            if pct>=3:      return "#0a5c2e","#00e676"
            elif pct>=1.5:  return "#145a32","#69f0ae"
            elif pct>=0.5:  return "#1e4d2b","#a5d6a7"
            elif pct>=0:    return "#1b3a28","#c8e6c9"
            elif pct>=-0.5: return "#4a1010","#ef9a9a"
            elif pct>=-1.5: return "#6b1414","#e57373"
            elif pct>=-3:   return "#8b1a1a","#f44336"
            else:           return "#b71c1c","#ff1744"

        bulls = sum(1 for _,_,p in heatmap_rows if p>=0)
        c1,c2,c3 = st.columns(3)
        c1.metric("🟢 Advancing", bulls)
        c2.metric("🔴 Declining", len(heatmap_rows)-bulls)
        c3.metric("📊 Total", len(heatmap_rows))
        tiles_html = """<style>
        .heatmap-grid{display:flex;flex-wrap:wrap;gap:6px;padding:10px 0}
        .hm-tile{width:110px;min-height:70px;border-radius:6px;padding:8px 6px;
            display:flex;flex-direction:column;justify-content:center;align-items:center;
            font-family:'Segoe UI',sans-serif;box-shadow:0 1px 4px rgba(0,0,0,.4)}
        .hm-sym{font-size:11px;font-weight:700;letter-spacing:.5px}
        .hm-pct{font-size:15px;font-weight:800;margin:2px 0}
        .hm-price{font-size:10px;opacity:.85}
        </style><div class="heatmap-grid">"""
        for sym,price,pct in heatmap_rows:
            bg,fg = tile_color(pct)
            sign = "+" if pct>=0 else ""
            tiles_html += f'<div class="hm-tile" style="background:{bg};color:{fg};"><div class="hm-sym">{sym}</div><div class="hm-pct">{sign}{pct:.2f}%</div><div class="hm-price">₹{price:,.1f}</div></div>'
        tiles_html += "</div>"
        st.markdown(tiles_html, unsafe_allow_html=True)

    with menu[2]:
        st.subheader("🪤 Trap Detection")
        if trap:
            df = pd.DataFrame(trap, columns=["Symbol","Price (₹)","Trap Type"])
            st.warning(f"⚠️ {len(df)} trap(s) detected!")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No traps detected.")

    with menu[3]:
        st.subheader("💧 Liquidity Zones")
        if liquidity:
            df = pd.DataFrame(liquidity, columns=["Symbol","Price (₹)","Zone Level (₹)","Zone Type"])
            st.success(f"{len(df)} stocks near key liquidity zones")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No liquidity zone touches detected.")

    with menu[4]:
        st.subheader("📦 Order Block Detection")
        if order_blocks:
            df = pd.DataFrame(order_blocks, columns=["Symbol","Price (₹)","OB Open","OB Close","Type"])
            st.success(f"{len(df)} order blocks identified")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No clear order blocks found.")

    with menu[5]:
        st.subheader("💎 Smart Money Moves")
        if smart_money:
            df = pd.DataFrame(smart_money, columns=["Symbol","Price (₹)","Candle Size","Direction"])
            df = df.sort_values("Candle Size", ascending=False).reset_index(drop=True)
            st.success(f"{len(df)} smart money impulses detected")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No smart money moves detected.")

    with menu[6]:
        st.subheader("📥 Accumulation Zones")
        if accumulation:
            df = pd.DataFrame(accumulation, columns=["Symbol","Price (₹)","Price Range %"])
            df = df.sort_values("Price Range %").reset_index(drop=True)
            st.success(f"{len(df)} stocks in accumulation")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No accumulation zones found.")

    with menu[8]:
        st.subheader("📈 Technical Indicators (EMA + RSI)")
        if technical:
            df = pd.DataFrame(technical, columns=["Symbol","Price (₹)","EMA9","EMA21","RSI","Signal"])
            df = df.sort_values("RSI").reset_index(drop=True)
            st.dataframe(df.style.map(
                lambda v: "background-color:#1a3a1a;color:lightgreen" if v=="BUY"
                else ("background-color:#3a1a1a;color:#ff6b6b" if v=="SELL" else ""),
                subset=["Signal"]), use_container_width=True)
        else:
            st.warning("No technical data available.")

    with menu[9]:
        st.subheader("🚀 Breakouts (20-period High)")
        if breakout:
            df = pd.DataFrame(breakout, columns=["Symbol","Price (₹)","20H Level (₹)","Breakout %"])
            df = df.sort_values("Breakout %", ascending=False).reset_index(drop=True)
            st.success(f"{len(df)} breakout(s) detected!")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No breakouts detected currently.")

    with menu[10]:
        st.subheader("🎯 Pivot Points (Classic)")
        if pivot_data:
            df = pd.DataFrame(pivot_data, columns=["Symbol","Price (₹)","PP","S2","S1","R1","R2","Position"])
            st.success(f"Pivot levels for {len(df)} stocks")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No pivot data available.")

else:
    for i, tab in enumerate(menu):
        if i == 7: continue  # volume tab has own state
        with tab:
            st.info("🔍 Select a market and press **▶ RUN SCAN** to begin analysis.")

st.markdown("---")
st.caption("📡 DevoteFX PRO | Data: Yahoo Finance | NSE/BSE: 9:15–15:30 IST | MCX: 9:00–23:30 IST | ⚠️ Educational use only.")
