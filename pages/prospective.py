import streamlit as st
import pandas as pd
import numpy as np
import os, sys

# Ensure root folder is in Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_model


def render():

    # ---------------------------------------------------------
    # EXECUTIVE THEME (same as Business Impact & Batch Scoring)
    # ---------------------------------------------------------
    st.markdown("""
<style>
.main, .block-container { background-color: #F2F2F2 !important; }

.block {
    background-color: #FFFFFF;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 28px;
}

.section-header {
    background-color: #2A4B8D;
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 18px;
}

.subsection-title {
    color: #2A4B8D;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

.bullet-text {
    color: #2A4B8D;
    font-size: 15px;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TITLE BLOCK
    # ---------------------------------------------------------
    st.markdown("""
<div class="section-header" style="font-size:26px;">
    Prospective Forecast (Next 12 Months)
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown("""
<div class="bullet-text" style="font-size:16px;">
Upload a <b>customer-level dataset</b> to generate a population-level churn and revenue forecast.
<br><br>
This module estimates:
<br><br>
🔵 Expected churners<br>
🔵 Revenue at risk<br>
🔵 Revenue saved<br>
🔵 Base / Optimistic / Pessimistic scenarios<br><br>
Ideal for strategic planning, budgeting, and executive forecasting.
</div>
""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # FILE UPLOADER
    # ---------------------------------------------------------
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">Upload Customer Dataset (CSV)</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Customer Dataset", type=["csv"])

    st.markdown("""
<p style='font-size:13px; color:#2A4B8D; margin-top:5px;'>
Required columns:<br>
<b>total_secs</b>, <b>has_auto_renew</b>, <b>has_cancelled</b>, 
<b>customer_tenure_days</b>, <b>city_grouped</b>, <b>payment_variability</b>,<br>
<b>avg_amount_paid</b>, <b>total_amount_paid</b>, <b>num_unq</b>,
<b>gender</b>, <b>age</b>, <b>registered_via_grouped</b>, <b>listening_group</b>
</p>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is None:
        st.info("Please upload a CSV file to generate the forecast.")
        return

    # ---------------------------------------------------------
    # LOAD MODEL + PROCESS FILE
    # ---------------------------------------------------------
    try:
        model = load_model()

        expected_features = [
            "gender", "age", "city_grouped", "registered_via_grouped",
            "avg_amount_paid", "total_amount_paid",
            "has_auto_renew", "has_cancelled",
            "total_secs", "num_unq",
            "customer_tenure_days", "listening_group",
            "payment_variability"
        ]

        df = pd.read_csv(uploaded_file)

        missing = [c for c in expected_features if c not in df.columns]
        if missing:
            st.error(f"Missing required columns: {missing}")
            return

        df["churn_prob"] = model.predict_proba(df[expected_features])[:, 1]

        ARPU = df["avg_amount_paid"].mean()
        expected_churners = int(df["churn_prob"].mean() * len(df))
        revenue_at_risk = expected_churners * ARPU

        scenarios = pd.DataFrame({
            "Scenario": ["Base", "Optimistic", "Pessimistic"],
            "Expected_Churners (customers)": [
                expected_churners,
                int(expected_churners * 0.9),
                int(expected_churners * 1.2)
            ],
            "Revenue_at_Risk (€)": [
                int(revenue_at_risk),
                int(revenue_at_risk * 0.9),
                int(revenue_at_risk * 1.2)
            ],
            "Revenue_Saved (€)": [
                int(revenue_at_risk * 0.10),
                int(revenue_at_risk * 0.15),
                int(revenue_at_risk * 0.05)
            ]
        })

    except Exception as e:
        st.error(f"Error computing forecast: {e}")
        return

    # ---------------------------------------------------------
    # FORECAST SCENARIOS BLOCK
    # ---------------------------------------------------------
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Forecast Scenarios</div>', unsafe_allow_html=True)

    st.dataframe(scenarios, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # EXECUTIVE INSIGHT BLOCK
    # ---------------------------------------------------------
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Executive Insight</div>', unsafe_allow_html=True)

    st.markdown(f"""
<div class="bullet-text">
• Base case forecasts <b>{expected_churners:,}</b> churners.<br>
• Revenue at risk exceeds <b>€{int(revenue_at_risk):,}</b>.<br>
• Optimistic conditions still expose the business to significant loss.<br>
• Targeted retention can recover up to <b>€{int(revenue_at_risk*0.15):,}</b>.<br>
• Churn is a multi‑million‑euro leak that can be contained with focused action.
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)