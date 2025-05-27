import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os

st.set_page_config(page_title="Luna Lira", layout="wide")

# Header with logo
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://raw.githubusercontent.com/DuncanEdward/LunaLiraAssets/main/LunaLiraLogo.png", width=100)
with col2:
    st.title("Luna Lira: Astro-Financial Signal App")

st.markdown("---")

# Premium access toggle
st.sidebar.header("🔐 Access")
user_code = st.sidebar.text_input("Enter access code to unlock premium features", type="password")
is_premium = (user_code == "PREMIUM123")

if is_premium:
    st.sidebar.success("✅ Premium Access Granted")
else:
    st.sidebar.info("Free access: showing 1 signal")

# Dynamic Daily Signal
st.subheader("🔮 Today's Astro Signal Preview")

today = datetime.today()
mock_ipos = {
    "AAPL": datetime(1980, 12, 12),
    "TSLA": datetime(2010, 6, 29),
    "NVDA": datetime(1999, 1, 22)
}
mock_highs = {
    "AMZN": datetime(2023, 8, 15),
    "GOOGL": datetime(2022, 12, 5),
    "MSFT": datetime(2023, 10, 18)
}

signals_today = []

for stock, ipo_date in mock_ipos.items():
    for year in range(1, 6):
        return_date = ipo_date + timedelta(days=365.25 * year)
        if abs((today - return_date).days) <= 3:
            signals_today.append(f"☀️ Sun Return for {stock} ({year}y since IPO)")

for stock, high_date in mock_highs.items():
    for cycle in range(1, 4):
        return_date = high_date + timedelta(days=27.33 * cycle)
        if abs((today - return_date).days) <= 2:
            signals_today.append(f"🌕 Moon Return for {stock} ({cycle} cycles since high)")

if signals_today:
    shown_signals = signals_today if is_premium else signals_today[:1]
    for signal in shown_signals:
        st.success(signal)
    if not is_premium and len(signals_today) > 1:
        st.warning("Upgrade to premium for more signals.")
else:
    st.info("No current sun or moon return signals detected.")

st.markdown("---")

# IPO Return Input
st.subheader("☀️ Solar Return from IPO Date")
ipo_input = st.text_area("Enter IPO Dates (YYYY-MM-DD, one per line):")
if ipo_input:
    try:
        dates = [pd.to_datetime(date.strip()) for date in ipo_input.splitlines()]
        df = pd.DataFrame({"IPO Date": dates})
        df["Sun Return 1"] = df["IPO Date"] + pd.to_timedelta(365.25, unit="D")
        df["Sun Return 2"] = df["IPO Date"] + pd.to_timedelta(2*365.25, unit="D")
        st.dataframe(df)
    except Exception:
        st.error("⚠️ Invalid date format. Use YYYY-MM-DD.")

# Moon Return Input
st.subheader("🌕 Moon Return from Market Highs")
high_input = st.text_area("Enter Market High Dates (YYYY-MM-DD, one per line):")
if high_input:
    try:
        highs = [pd.to_datetime(date.strip()) for date in high_input.splitlines()]
        moon_df = pd.DataFrame({"High Date": highs})
        moon_df["Moon Return 1"] = moon_df["High Date"] + pd.to_timedelta(27.33, unit="D")
        moon_df["Moon Return 2"] = moon_df["High Date"] + pd.to_timedelta(54.66, unit="D")
        st.dataframe(moon_df)
    except Exception:
        st.error("⚠️ Invalid date format. Use YYYY-MM-DD.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:14px; color:gray;'>"
    "Luna Lira — Financial Analysis, the Esoteric Way • © 2025"
    "</div>",
    unsafe_allow_html=True
)
