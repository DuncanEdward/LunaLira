import streamlit as st
from datetime import datetime
import os
import base64
from email.message import EmailMessage
import requests

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

st.set_page_config(page_title="Luna Lira", layout="centered")
st.title("📧 Luna Lira Alerts Sender")

# Load subscribers from encrypted file
try:
    with open("subscribers.dat", "rb") as f:
        decrypted = f.read().decode(errors="ignore")
        subscribers = [line.strip() for line in decrypted.splitlines() if '@' in line]
except Exception:
    subscribers = []

today = datetime.today().strftime("%B %d, %Y")

st.write(f"Total subscribers: {len(subscribers)}")

# Select signal content
free_signal = "Sun Return for AAPL"
premium_signals = [
    "Sun Return for AAPL",
    "Moon Return for AMZN",
    "Moon Return for MSFT"
]

# Allow user to simulate Send
if st.button("📤 Send Alerts Now"):
    if not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
        st.error("Missing SendGrid credentials. Please set in environment variables.")
    else:
        success_count = 0
        fail_count = 0

        for email in subscribers:
            is_premium = "premium" in email.lower()
            msg = EmailMessage()
            msg["From"] = SENDGRID_FROM_EMAIL
            msg["To"] = email
            msg["Subject"] = f"Luna Lira Alert — {today}"

            if is_premium:
                body = f"Luna Lira — Financial Analysis, the Esoteric Way\n\nDate: {today}\n\n"
                body += "Premium Signals:\n" + "\n".join(f"- {s}" for s in premium_signals)
                body += "\n\nPDF report attached.\n\nThank you for subscribing!\nLuna Lira Team"
                msg.set_content(body)

                # Attach PDF if exists
                pdf_path = "luna_lira_report_with_charts.pdf"
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_encoded = base64.b64encode(f.read()).decode()
                    attachment = {
                        "content": pdf_encoded,
                        "type": "application/pdf",
                        "filename": "LunaLira_Report.pdf"
                    }
                else:
                    attachment = None
            else:
                body = f"Luna Lira — Financial Analysis, the Esoteric Way\n\nDate: {today}\n\n"
                body += f"Today's Signal: {free_signal}\n\n"
                body += "Upgrade for full access:\nhttps://lunalira.onrender.com"
                msg.set_content(body)
                attachment = None

            data = {
                "personalizations": [{"to": [{"email": email}], "subject": msg["Subject"]}],
                "from": {"email": msg["From"]},
                "content": [{"type": "text/plain", "value": msg.get_content()}]
            }

            if is_premium and attachment:
                data["attachments"] = [attachment]

            headers = {
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
            if response.status_code == 202:
                success_count += 1
            else:
                fail_count += 1
                st.warning(f"Failed for {email}: {response.text}")

        st.success(f"✅ Sent {success_count} alerts successfully. {fail_count} failed.")
