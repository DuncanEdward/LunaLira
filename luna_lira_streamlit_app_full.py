# luna_lira_streamlit_app.py (Final Full Version)

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Luna Lira", layout="wide")
st.title("Luna Lira: Astro-Financial Signal App")

# IPO Solar Return Section
st.header("☀️ Solar Return from IPO Date")
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

# Moon Return Section
st.header("🌕 Moon Return from Market Highs")
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

# 50-Day Moving Average Pullback Alerts (Simulated)
st.header("📉 Pullback Near 50-Day MA (Simulated Data)")
symbols = ["AAPL", "TSLA", "NVDA", "AMZN"]
for symbol in symbols:
    prices = np.random.normal(loc=150 + random.randint(-50, 50), scale=5, size=60)
    ma50 = pd.Series(prices).rolling(50).mean()
    if abs(prices[-1] - ma50.iloc[-1]) / ma50.iloc[-1] < 0.01:
        st.warning(f"🔔 {symbol} is approaching 50-day MA!")

# Reversal Alerts from Key Degrees (Simulated)
st.header("⚠️ Reversal Watch (Simulated Astro Degrees)")
sensitive_degrees = {"Cancer": 14, "Pisces": 24, "Virgo": 18, "Libra": 27}
sun_sign = random.choice(list(sensitive_degrees))
sun_deg = sensitive_degrees[sun_sign] - random.uniform(0, 2)
moon_sign = random.choice(list(sensitive_degrees))
moon_deg = sensitive_degrees[moon_sign] - random.uniform(0, 2)

alerts = []
if sun_deg < sensitive_degrees[sun_sign]:
    alerts.append(f"☀️ Sun applying to {sensitive_degrees[sun_sign]}° {sun_sign}")
if moon_deg < sensitive_degrees[moon_sign]:
    alerts.append(f"🌙 Moon applying to {sensitive_degrees[moon_sign]}° {moon_sign}")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("✅ No sensitive degree reversals at this time.")

# Signal Scoring (Mock)
st.header("🎯 Trade Signal Scoring (Mocked)")
score_factors = ["Moon Return", "50 MA Pullback", "Sensitive Degree", "Sun Return"]
scores = {factor: random.choice([0, 1]) for factor in score_factors}
total_score = sum(scores.values())
st.write(f"**Signal Score:** {total_score}/4")
st.json(scores)

# Placeholder for future email & PDF export
st.markdown("---")
st.caption("📬 Email alert system and PDF exports available in premium release.")
