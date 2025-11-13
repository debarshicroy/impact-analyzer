import streamlit as st
from backend import analyze_impact
import json

st.set_page_config(page_title="AI Impact Analyzer", layout="centered")
st.title("🧠 AI Requirement Impact Analyzer")

st.markdown("Enter a new or modified requirement to analyze possible system impacts.")

req_text = st.text_area("Enter Requirement", height=150)

if st.button("Analyze Impact"):
    if req_text.strip():
        with st.spinner("Analyzing..."):
            output = analyze_impact(req_text)
        st.subheader("Impact Analysis Report")
        st.json(output)
    else:
        st.warning("Please enter a requirement text first.")
