# luna_lira_streamlit_app.py (with SendGrid Email Feature Enabled)

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import requests
import base64
import os

st.set_page_config(page_title="Luna Lira", layout="wide")
st.title("Luna Lira: Astro-Financial Signal App")

# IPO Solar Return
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

# Moon Return
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

# Signal Summary
st.header("🎯 Signal Summary")
summary = "Luna Lira Daily Signal Summary\n"
summary += "Sun Return Dates and Moon Returns from highs have been calculated.\n"
summary += "Sensitive degrees and technical conditions are under monitoring."

st.code(summary)

# Send Email Section
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")

to_email = st.text_input("📬 Send alert to (email address):")

if st.button("📤 Send Daily Summary via SendGrid"):
    if not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
        st.error("SendGrid environment variables not set.")
    elif not to_email:
        st.error("Please enter a recipient email.")
    else:
        try:
            data = {
                "personalizations": [
                    {
                        "to": [{"email": to_email}],
                        "subject": "Luna Lira Daily Astro Signal"
                    }
                ],
                "from": {"email": SENDGRID_FROM_EMAIL},
                "content": [
                    {
                        "type": "text/plain",
                        "value": summary
                    }
                ]
            }
            headers = {
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
            if response.status_code == 202:
                st.success("📧 Email sent successfully!")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
