import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
import os

# ---- Branding and Layout Styling ----
st.set_page_config(page_title="Luna Lira", layout="wide")

# Header layout with logo
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://raw.githubusercontent.com/DuncanEdward/LunaLiraAssets/main/LunaLiraLogo.png", width=100)
with col2:
    st.title("Luna Lira: Astro-Financial Signal App")

st.markdown("---")

# IPO Solar Return
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

# Moon Return
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

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:14px; color:gray;'>"
    "Luna Lira — Financial Analysis, the Esoteric Way • © 2025"
    "</div>",
    unsafe_allow_html=True
)
