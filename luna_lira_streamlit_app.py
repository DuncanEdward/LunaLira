import streamlit as st
import os

st.set_page_config(page_title="Luna Lira Debug", layout="centered")
st.title("🔍 Luna Lira: SendGrid Debug")

# Retrieve environment variables
api_key = os.getenv("SENDGRID_API_KEY", None)
from_email = os.getenv("SENDGRID_FROM_EMAIL", None)

# Display debug info
st.header("🔧 SendGrid Environment Variable Check")
st.write("**SENDGRID_API_KEY loaded:**", bool(api_key))
st.write("**SENDGRID_FROM_EMAIL loaded:**", bool(from_email))

if api_key:
    st.success("✅ SENDGRID_API_KEY is set.")
else:
    st.error("❌ SENDGRID_API_KEY is NOT set.")

if from_email:
    st.success(f"✅ SENDGRID_FROM_EMAIL is set to: `{from_email}`")
else:
    st.error("❌ SENDGRID_FROM_EMAIL is NOT set.")
