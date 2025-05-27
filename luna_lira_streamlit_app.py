import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import base64
import requests
from email.message import EmailMessage
from fpdf import FPDF

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

st.set_page_config(page_title="Luna Lira", layout="wide")

col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://raw.githubusercontent.com/DuncanEdward/LunaLiraAssets/main/LunaLiraLogo.png", width=100)
with col2:
    st.title("Luna Lira: Astro-Financial Signal App")

st.markdown("---")
st.sidebar.header("🔐 Access")

user_code = st.sidebar.text_input("Enter access code", type="password")
is_premium = user_code == "PREMIUM123"
is_admin = user_code == "ADMIN321"

if is_premium:
    st.sidebar.success("✅ Premium Access")
elif is_admin:
    st.sidebar.success("🔧 Admin Access")
else:
    st.sidebar.info("Free access: limited signals")

# --- Signal Logic ---
today = datetime.today()
mock_ipos = {"AAPL": datetime(1980, 12, 12)}
mock_highs = {"AMZN": datetime(2023, 8, 15), "MSFT": datetime(2023, 10, 18)}
signals_today = []

def plot_chart(symbol, label, date):
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

for stock, ipo in mock_ipos.items():
    if abs((today - (ipo + timedelta(days=365.25))).days) <= 3:
        signals_today.append(("Sun Return", stock, today))
for stock, high in mock_highs.items():
    if abs((today - (high + timedelta(days=27.33))).days) <= 2:
        signals_today.append(("Moon Return", stock, today))

st.subheader("🔮 Today's Astro Signal Preview")
visible = signals_today if is_premium or is_admin else signals_today[:1]
for label, stock, date in visible:
    st.success(f"{label} for {stock} on {date.strftime('%b %d, %Y')}")
    if is_premium or is_admin:
        st.image(plot_chart(stock, label, date), caption=f"{stock} — {label}", use_column_width=True)

# --- PDF Export ---
if (is_premium or is_admin) and signals_today:
    if st.button("📄 Download PDF with Charts"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Luna Lira Daily Astro-Financial Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Date: {today.strftime('%B %d, %Y')}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.ln(5)
        pdf.cell(200, 10, "Today's Signals:", ln=True)
        charts = []
        for label, stock, date in signals_today:
            pdf.cell(200, 10, f"- {label} for {stock}", ln=True)
            charts.append((plot_chart(stock, label, date), f"{stock} — {label}"))
        for path, title in charts:
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            safe_title = title.encode("latin-1", "replace").decode("latin-1")
            pdf.cell(200, 10, safe_title, ln=True, align="C")
            pdf.image(path, x=10, y=30, w=190)
        pdf_file = "/mnt/data/luna_lira_report.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="luna_lira_report.pdf", mime="application/pdf")

# --- Admin Email Alert Panel ---
if is_admin:
    st.markdown("---")
    st.subheader("📧 Send Daily Alerts to Subscribers")

    try:
        with open("subscribers.dat", "rb") as f:
            decrypted = f.read().decode(errors="ignore")
            emails = [line.strip() for line in decrypted.splitlines() if '@' in line]
    except Exception:
        emails = []

    st.write(f"Total subscribers: {len(emails)}")

    if st.button("🚀 Send Alerts Now"):
        if not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
            st.error("SendGrid credentials not set.")
        else:
            sent, failed = 0, 0
            for email in emails:
                is_premium_user = "premium" in email.lower()
                msg = EmailMessage()
                msg["From"] = SENDGRID_FROM_EMAIL
                msg["To"] = email
                msg["Subject"] = f"Luna Lira Alert — {today.strftime('%B %d, %Y')}"

                if is_premium_user:
                    body = f"Luna Lira Premium Signals\n\nDate: {today.strftime('%B %d, %Y')}\n"
                    for s in signals_today:
                        body += f"- {s[0]} for {s[1]}\n"
                    body += "\nPDF attached.\nThank you!"
                    msg.set_content(body)

                    if os.path.exists("/mnt/data/luna_lira_report.pdf"):
                        with open("/mnt/data/luna_lira_report.pdf", "rb") as f:
                            encoded = base64.b64encode(f.read()).decode()
                        attach = {
                            "content": encoded,
                            "type": "application/pdf",
                            "filename": "LunaLira_Report.pdf"
                        }
                    else:
                        attach = None
                else:
                    body = f"Luna Lira Signal\nDate: {today.strftime('%B %d, %Y')}\n- {signals_today[0][0]} for {signals_today[0][1]}\nUpgrade at https://lunalira.onrender.com"
                    msg.set_content(body)
                    attach = None

                data = {
                    "personalizations": [{"to": [{"email": email}], "subject": msg["Subject"]}],
                    "from": {"email": msg["From"]},
                    "content": [{"type": "text/plain", "value": msg.get_content()}]
                }

                if is_premium_user and attach:
                    data["attachments"] = [attach]

                headers = {
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
                if response.status_code == 202:
                    sent += 1
                else:
                    failed += 1
                    st.warning(f"Failed for {email}: {response.text}")

            st.success(f"✅ Sent: {sent}, Failed: {failed}")
st.markdown("---")
st.markdown("<div style='text-align:center; font-size:12px; color:gray;'>Luna Lira — Financial Analysis, the Esoteric Way © 2025</div>", unsafe_allow_html=True)
