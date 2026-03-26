import streamlit as st
import pandas as pd
from detection.fusion_score import fusion_detection

st.title("🚨 Log-Based Intrusion Detection System")

file = st.file_uploader("Upload log features CSV")

if file:
    df = pd.read_csv(file)

    results = fusion_detection(df)

    st.subheader("Detection Results")
    st.write(results.head())

    st.subheader("🚨 Detected Attacks")
    attacks = results[results["fusion_flag"] == 1]

    st.write(attacks[["ip", "fusion_score", "attack_reason"]])