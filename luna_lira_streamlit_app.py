import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="Luna Lira", layout="wide")

col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://raw.githubusercontent.com/DuncanEdward/LunaLiraAssets/main/LunaLiraLogo.png", width=100)
with col2:
    st.title("Luna Lira: Astro-Financial Signal App")

st.markdown("---")

st.sidebar.header("🔐 Access")
user_code = st.sidebar.text_input("Enter access code to unlock premium features", type="password")
is_premium = (user_code == "PREMIUM123")

if is_premium:
    st.sidebar.success("✅ Premium Access Granted")
else:
    st.sidebar.info("Free access: showing 1 signal")

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
    ax.plot(dates, prices, label="Price")
    ax.axvline(date, color="red", linestyle="--", label=label)
    ax.set_title(f"{symbol} — {label}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    plt.xticks(rotation=45)
    fig.tight_layout()
    chart_path = f"/mnt/data/{symbol}_{label.replace(' ', '_')}_chart.png"
    fig.savefig(chart_path)
    plt.close(fig)
    return chart_path

for stock, ipo_date in mock_ipos.items():
    for year in range(1, 6):
        return_date = ipo_date + timedelta(days=365.25 * year)
        if abs((today - return_date).days) <= 3:
            signals_today.append(("Sun Return", stock, return_date))

for stock, high_date in mock_highs.items():
    for cycle in range(1, 4):
        return_date = high_date + timedelta(days=27.33 * cycle)
        if abs((today - return_date).days) <= 2:
            signals_today.append(("Moon Return", stock, return_date))

st.subheader("🔮 Today's Astro Signal Preview")
if signals_today:
    shown = signals_today if is_premium else signals_today[:1]
    for label, stock, date in shown:
        st.success(f"{label} for {stock} on {date.strftime('%b %d, %Y')}")
        if is_premium:
            chart_file = plot_mock_chart(stock, label, date)
            st.image(chart_file, caption=f"{stock} — {label}", use_column_width=True)
    if not is_premium and len(signals_today) > 1:
        st.warning("Upgrade to premium for more signals and charts.")
else:
    st.info("No current sun or moon return signals detected.")

# PDF Export with charts
if is_premium and signals_today:
    if st.button("📄 Download Today's PDF Report (with Charts)"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Luna Lira Daily Astro-Financial Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "I", 12)
        pdf.cell(200, 10, "Powered by Luna Lira: Financial Analysis, the Esoteric Way", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Date: {today.strftime('%B %d, %Y')}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "", 11)
        pdf.cell(200, 10, "Today's Signals:", ln=True)
        chart_paths = []
        for label, stock, date in signals_today:
            pdf.cell(200, 10, f"- {label} for {stock} on {date.strftime('%B %d, %Y')}", ln=True)
            chart_path = plot_mock_chart(stock, label, date)
            chart_paths.append((chart_path, f"{stock} — {label}"))
        pdf.ln(10)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(200, 10, "This report was generated automatically by Luna Lira.", ln=True, align="C")

        for chart_path, title in chart_paths:
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            safe_title = title.encode("latin-1", "replace").decode("latin-1")
            pdf.cell(200, 10, safe_title, ln=True, align="C")
            pdf.image(chart_path, x=10, y=30, w=190)

        report_path = "/mnt/data/luna_lira_report_with_charts.pdf"
        pdf.output(report_path)
        with open(report_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="luna_lira_report_with_charts.pdf", mime="application/pdf")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:14px; color:gray;'>"
    "Luna Lira — Financial Analysis, the Esoteric Way • © 2025"
    "</div>",
    unsafe_allow_html=True
)
