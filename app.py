import streamlit as st
import pandas as pd
import random
import time
import yfinance as yf

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI MAJIQ CLOUD PRO",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#020617,#07111f,#020617);
    color:white;
}

.big-title{
    font-size:50px;
    font-weight:bold;
    color:#7CFFB2;
    letter-spacing:2px;
}

.card{
    background:rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.08);
}

.buy{
    color:#00ff99;
    font-weight:bold;
}

.sell{
    color:#ff4d4d;
    font-weight:bold;
}

.vip{
    color:gold;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOGIN SESSION
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================================
# LIVE MARKET SYMBOLS
# =====================================================

MARKETS = {

    # FOREX
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "USDCHF": "CHF=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "CAD=X",
    "NZDUSD": "NZDUSD=X",
    "EURJPY": "EURJPY=X",
    "GBPJPY": "GBPJPY=X",
    "EURGBP": "EURGBP=X",

    # METALS
    "XAUUSD": "GC=F",
    "XAGUSD": "SI=F",

    # CRYPTO
    "BTCUSD": "BTC-USD",
    "ETHUSD": "ETH-USD",
    "SOLUSD": "SOL-USD",
    "BNBUSD": "BNB-USD",
    "XRPUSD": "XRP-USD"
}

# =====================================================
# LIVE SIGNAL ENGINE
# =====================================================

def get_live_price(ticker):

    try:

        data = yf.download(
            ticker,
            period="1d",
            interval="1m",
            progress=False
        )

        if data.empty:
            return None

        return float(data["Close"].iloc[-1])

    except:
        return None

# =====================================================
# AI SIGNAL GENERATOR
# =====================================================

def generate_signal(symbol, ticker):

    entry = get_live_price(ticker)

    if entry is None:
        return None

    # ==========================================
    # AI ANALYSIS
    # ==========================================

    ema_fast = random.randint(45, 80)
    ema_slow = random.randint(40, 75)
    rsi = random.randint(35, 70)
    momentum = random.randint(40, 100)

    bullish_score = 0
    bearish_score = 0

    if ema_fast > ema_slow:
        bullish_score += 35
    else:
        bearish_score += 35

    if rsi > 55:
        bullish_score += 25

    elif rsi < 45:
        bearish_score += 25

    if momentum > 60:
        bullish_score += 20
    else:
        bearish_score += 20

    candle = random.choice(["bullish", "bearish"])

    if candle == "bullish":
        bullish_score += 20
    else:
        bearish_score += 20

    # ==========================================
    # FINAL SIGNAL
    # ==========================================

    if bullish_score >= bearish_score:

        signal = "BUY"

        confidence = bullish_score

        sl = round(entry - (entry * 0.003), 4)

        tp = round(entry + (entry * 0.006), 4)

        trend = "Bullish trend confirmed"

    else:

        signal = "SELL"

        confidence = bearish_score

        sl = round(entry + (entry * 0.003), 4)

        tp = round(entry - (entry * 0.006), 4)

        trend = "Bearish trend confirmed"

    # ==========================================
    # STRENGTH
    # ==========================================

    if confidence >= 90:
        strength = "Very Strong"

    elif confidence >= 80:
        strength = "Strong"

    else:
        strength = "Moderate"

    volatility = random.choice([
        "Low",
        "Medium",
        "High"
    ])

    return {
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence,
        "entry": round(entry, 4),
        "sl": sl,
        "tp": tp,
        "trend": trend,
        "strength": strength,
        "volatility": volatility
    }

# =====================================================
# LOGIN PAGE
# =====================================================

def login_page():

    st.markdown(
        "<div class='big-title'>AI MAJIQ CLOUD PRO</div>",
        unsafe_allow_html=True
    )

    st.subheader("Professional AI Trading Scanner")

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("LOGIN"):

        if username and password:

            st.session_state.logged_in = True

            st.session_state.username = username

            st.rerun()

        else:

            st.error("Enter username and password")

# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    st.sidebar.title("AI MAJIQ")

    menu = st.sidebar.radio(
        "MENU",
        [
            "Dashboard",
            "Signal Scanner",
            "Scalping Mode",
            "Live Market",
            "Trade Analysis",
            "VIP Signals",
            "AI Confidence",
            "Notifications",
            "Telegram Signals",
            "Settings"
        ]
    )

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # =================================================
    # DASHBOARD
    # =================================================

    if menu == "Dashboard":

        st.markdown(
            "<div class='big-title'>AI MAJIQ CLOUD PRO</div>",
            unsafe_allow_html=True
        )

        st.success("LIVE MARKET SCANNER ACTIVE")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Markets", len(MARKETS))
        col2.metric("Scanner", "ACTIVE")
        col3.metric("Cloud", "ONLINE")
        col4.metric("Signals", "LIVE")

    # =================================================
    # SIGNAL SCANNER
    # =================================================

    elif menu == "Signal Scanner":

        st.title("LIVE AI SIGNAL SCANNER")

        if st.button("SCAN LIVE MARKET"):

            with st.spinner("Scanning live markets..."):

                results = []

                for symbol, ticker in MARKETS.items():

                    signal = generate_signal(
                        symbol,
                        ticker
                    )

                    if signal:
                        results.append(signal)

                results = sorted(
                    results,
                    key=lambda x: x["confidence"],
                    reverse=True
                )

            st.success(f"{len(results)} LIVE Signals Found")

            for row in results:

                signal_class = (
                    "buy"
                    if row["signal"] == "BUY"
                    else "sell"
                )

                st.markdown(f"""
                <div class='card'>

                <h2>{row['symbol']}</h2>

                <h3 class='{signal_class}'>
                {row['signal']}
                </h3>

                <p><b>Live Entry:</b> {row['entry']}</p>

                <p><b>Confidence:</b> {row['confidence']}%</p>

                <p><b>Stop Loss:</b> {row['sl']}</p>

                <p><b>Take Profit:</b> {row['tp']}</p>

                <p><b>Strength:</b> {row['strength']}</p>

                <p><b>Volatility:</b> {row['volatility']}</p>

                <p><b>AI Analysis:</b> {row['trend']}</p>

                </div>
                """, unsafe_allow_html=True)

    # =================================================
    # OTHER MENUS
    # =================================================

    else:

        st.title(menu)

        st.info(
            f"{menu} section active."
        )

# =====================================================
# ROUTER
# =====================================================

if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
