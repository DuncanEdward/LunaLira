import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

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

def plot_mock_chart(symbol, label, date):
    dates = pd.date_range(start=date - timedelta(days=30), end=date + timedelta(days=30))
    prices = np.random.normal(loc=100, scale=3, size=len(dates))
    fig, ax = plt.subplots()
    ax.plot(dates, prices, label="Price", linewidth=2)
    ax.axvline(date, color="red", linestyle="--", label=label)
    title = f"{symbol} — {label}"
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

for stock, ipo_date in mock_ipos.items():
    for year in range(1, 6):
        return_date = ipo_date + timedelta(days=365.25 * year)
        if abs((today - return_date).days) <= 3:
            signals_today.append(("☀️ Sun Return", stock, return_date))

for stock, high_date in mock_highs.items():
    for cycle in range(1, 4):
        return_date = high_date + timedelta(days=27.33 * cycle)
        if abs((today - return_date).days) <= 2:
            signals_today.append(("🌕 Moon Return", stock, return_date))

if signals_today:
    shown = signals_today if is_premium else signals_today[:1]
    for label, stock, date in shown:
        st.success(f"{label} for {stock} on {date.strftime('%b %d, %Y')}")
        if is_premium:
            plot_mock_chart(stock, label, date)
    if not is_premium and len(signals_today) > 1:
        st.warning("Upgrade to premium for more signals and charts.")
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
