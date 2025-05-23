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

st.set_page_config(page_title="Luna Lira", layout="centered")

# Apply custom title
st.title("Luna Lira: Astro-Financial Signal App")

# Example section: IPO date analysis
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

# Add additional sections (Moon Returns, MA Pullbacks, Astro Scores) as needed.