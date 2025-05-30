import streamlit as st

st.title("🔐 Secrets Test")
st.write("🔍 GEMINI_API_KEY:", st.secrets.get("GEMINI_API_KEY", "❌ 없음"))
