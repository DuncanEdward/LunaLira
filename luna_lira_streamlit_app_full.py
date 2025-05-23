# luna_lira_streamlit_app.py

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random

st.set_page_config(page_title="Luna Lira", layout="wide")

st.title("Luna Lira: Astro-Financial Signal App")

# Section: Solar Return from IPO Dates
st.header("☀️ Solar Return from IPO Date")
ipo_input = st.text_area("Enter IPO Dates (YYYY-MM-DD, one per line):")

if ipo_input:
    try:
        dates = [pd.to_datetime(date.strip()) for date in ipo_input.splitlines()]
        df = pd.DataFrame({"IPO Date": dates})
        df["Sun Return 1"] = df["IPO Date"] + pd.to_timedelta(365.25, unit="D")
        df["Sun Return 2"] = df["IPO Date"] + pd.to_timedelta(2*365.25, unit="D")
        st.dataframe(df)
    except Exception as e:
        st.error("Could not parse dates. Ensure format is YYYY-MM-DD.")

# Section: Moon Return from Highs
st.header("🌕 Moon Return from Highs")
moon_highs = st.text_area("Enter Market High Dates (YYYY-MM-DD, one per line):")

if moon_highs:
    try:
        highs = [pd.to_datetime(d.strip()) for d in moon_highs.splitlines()]
        df = pd.DataFrame({"High Date": highs})
        df["Moon Return 1"] = df["High Date"] + pd.to_timedelta(27.33, unit="D")
        df["Moon Return 2"] = df["High Date"] + pd.to_timedelta(54.66, unit="D")
        st.dataframe(df)
    except Exception as e:
        st.error("Error with Moon Return Dates: check formatting.")

# Additional scoring, signal flags, and analytics features would follow here
# This keeps the deployed app clean and expandable