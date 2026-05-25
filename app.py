import streamlit as st
import yfinance as yf
from datetime import datetime
import time

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI MAJIQ CLOUD PRO",
    page_icon="📈",
    layout="wide"
)

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

.stApp{
    background:#020617;
    color:white;
}

.title{
    font-size:55px;
    font-weight:bold;
    color:#6effb2;
}

.card{
    background:#0f172a;
    padding:20px;
    border-radius:20px;
    margin-bottom:20px;
    border:1px solid #1e293b;
}

.buy{
    color:#00ff99;
    font-size:28px;
    font-weight:bold;
}

.sell{
    color:#ff4d4d;
    font-size:28px;
    font-weight:bold;
}

.neutral{
    color:orange;
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================

if "logged" not in st.session_state:
    st.session_state.logged = False

def login():

    st.markdown(
        '<p class="title">AI MAJIQ CLOUD PRO</p>',
        unsafe_allow_html=True
    )

    user = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("LOGIN"):

        if user and password:

            st.session_state.logged = True
            st.rerun()

        else:

            st.error("Enter username and password")

# ======================================================
# MARKETS
# ======================================================

markets = {

    # FOREX
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X",
    "USDJPY": "JPY=X",

    # METALS
    "XAUUSD": "GC=F",
    "XAGUSD": "SI=F",

    # CRYPTO
    "BTCUSD": "BTC-USD",
    "ETHUSD": "ETH-USD"
}

# ======================================================
# SIGNAL FUNCTION
# ======================================================

def scan_market(symbol, timeframe):

    try:

        # ==========================================
        # PERIOD FIX
        # ==========================================

        if timeframe == "5m":
            period = "1d"

        elif timeframe == "15m":
            period = "1d"

        elif timeframe == "30m":
            period = "5d"

        elif timeframe == "60m":
            period = "7d"

        else:
            period = "1mo"

        # ==========================================
        # DOWNLOAD
        # ==========================================

        data = yf.download(
            symbol,
            period=period,
            interval=timeframe,
            progress=False
        )

        # ==========================================
        # CHECK DATA
        # ==========================================

        if data.empty:
            return None

        # ==========================================
        # CLOSE PRICE
        # ==========================================

        close = float(data["Close"].iloc[-1])

        # ==========================================
        # EMA
        # ==========================================

        ema20 = float(
            data["Close"].ewm(span=20).mean().iloc[-1]
        )

        ema50 = float(
            data["Close"].ewm(span=50).mean().iloc[-1]
        )

        # ==========================================
        # SIGNAL
        # ==========================================

        signal = "NEUTRAL"

        if ema20 > ema50:
            signal = "BUY"

        elif ema20 < ema50:
            signal = "SELL"

        # ==========================================
        # TP / SL
        # ==========================================

        if signal == "BUY":

            tp = round(close * 1.01, 4)

            sl = round(close * 0.995, 4)

        elif signal == "SELL":

            tp = round(close * 0.99, 4)

            sl = round(close * 1.005, 4)

        else:

            tp = close
            sl = close

        # ==========================================
        # RETURN
        # ==========================================

        return {

            "price": round(close, 4),
            "signal": signal,
            "tp": tp,
            "sl": sl,
            "ema20": round(ema20, 4),
            "ema50": round(ema50, 4)
        }

    except:
        return None

# ======================================================
# DASHBOARD
# ======================================================

def dashboard():

    st.markdown(
        '<p class="title">LIVE AI SIGNAL SCANNER</p>',
        unsafe_allow_html=True
    )

    st.success("20+ UPGRADES ACTIVE")

    timeframe = st.selectbox(
        "Select Timeframe",
        ["5m", "15m", "30m", "60m", "1d"]
    )

    auto = st.checkbox("Auto Refresh")

    if auto:

        time.sleep(30)
        st.rerun()

    if st.button("SCAN LIVE MARKET"):

        count = 0

        for pair, ticker in markets.items():

            result = scan_market(
                ticker,
                timeframe
            )

            if result:

                count += 1

                # ===============================
                # COLOR
                # ===============================

                if result["signal"] == "BUY":
                    cls = "buy"

                elif result["signal"] == "SELL":
                    cls = "sell"

                else:
                    cls = "neutral"

                # ===============================
                # CARD
                # ===============================

                st.markdown(f"""

                <div class="card">

                <h2>{pair}</h2>

                <p class="{cls}">
                {result["signal"]}
                </p>

                <b>Live Entry:</b>
                {result["price"]}<br><br>

                <b>EMA20:</b>
                {result["ema20"]}<br>

                <b>EMA50:</b>
                {result["ema50"]}<br>

                <b>Take Profit:</b>
                {result["tp"]}<br>

                <b>Stop Loss:</b>
                {result["sl"]}<br>

                <b>Timeframe:</b>
                {timeframe}<br>

                <b>Updated:</b>
                {datetime.now().strftime("%H:%M:%S")}

                </div>

                """, unsafe_allow_html=True)

        st.success(f"{count} LIVE SIGNALS GENERATED")

# ======================================================
# ROUTER
# ======================================================

if st.session_state.logged:
    dashboard()
else:
    login()
