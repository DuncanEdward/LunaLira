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
    st.title("Luna Lira: Astro-Financial Signal App (Demo Mode)")

st.markdown("---")

# Premium access toggle
st.sidebar.header("🔐 Access")
user_code = st.sidebar.text_input("Enter access code to unlock premium features", type="password")
is_premium = (user_code == "PREMIUM123")

if is_premium:
    st.sidebar.success("✅ Premium Access Granted")
else:
    st.sidebar.info("Free access: limited signals shown")

# Today's Signal Simulation (Always Triggers for Demo)
st.subheader("🔮 Today's Astro Signal Preview (Demo)")
st.success("☀️ Sun Return for AAPL on " + datetime.today().strftime('%b %d, %Y'))

def plot_mock_chart(symbol, label, date):
    dates = pd.date_range(start=date - timedelta(days=30), end=date + timedelta(days=30))
    prices = np.random.normal(loc=100, scale=3, size=len(dates))
    fig, ax = plt.subplots()
    ax.plot(dates, prices, label="Price", linewidth=2)
    ax.axvline(date, color="red", linestyle="--", label=label)
    ax.set_title(f"{symbol} — {label}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

if is_premium:
    plot_mock_chart("AAPL", "☀️ Sun Return", datetime.today())
else:
    st.warning("Upgrade to Premium to view the chart.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:14px; color:gray;'>"
    "Luna Lira — Financial Analysis, the Esoteric Way • Demo © 2025"
    "</div>",
    unsafe_allow_html=True
)
