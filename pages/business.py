import streamlit as st
import plotly.express as px
import pandas as pd
from utils import score_customer, customer_input_sidebar


def render():

    # Executive Theme (CSS)
    
    st.markdown("""
<style>
/* GLOBAL BACKGROUND */
.main, .block-container {
    background-color: #F2F2F2 !important;
}

/* Floating white blocks */
.block {
    background-color: #FFFFFF;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 28px;
}

/* Section headers */
.section-header {
    background-color: #2A4B8D;
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 18px;
}

/* KPI cards */
.kpi-card {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0px 1px 6px rgba(0,0,0,0.06);
    margin-bottom: 6px;
    margin-top: 6px;
}

.kpi-title {
    color: #6E6E6E;
    font-size: 14px;
    margin-bottom: 4px;
}

.kpi-value {
    color: #1A1A1A;
    font-size: 22px;
    font-weight: 600;
}

/* LEARN MORE: TEXT-ONLY, TINY, NO BUTTON */
.learn-more {
    margin-top: 2px;
    text-align: left;
}

.learn-more summary {
    list-style: none;
    cursor: pointer;
    color: #8A8A8A;
    font-size: 9px;
    font-weight: 400;
    text-decoration: underline;
    text-underline-offset: 2px;
    display: inline-block;
}

.learn-more summary::-webkit-details-marker {
    display: none;
}

.learn-more-panel {
    margin-top: 6px;
    background-color: #2A3B4D;
    color: #FFFFFF;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12px;
    text-align: left;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
}
</style>
""", unsafe_allow_html=True)

    
    # Title Block

    st.markdown("""
<div class="section-header" style="font-size:26px;">
    Business Impact
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown("""
<span style="color:#2A4B8D; font-size:16px; line-height:1.55;">

This layer quantifies the **financial implications** of churn for a specific customer.  
It helps answer key business questions:

  🔵 How much revenue is at risk?  
  🔵 What is the customer's ARPU and LTV?  
  🔵 What is the potential financial upside of preventing churn?  
  🔵 How does this customer compare to retention benchmarks?  

</span>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    
    # Inputs
    
    input_data = customer_input_sidebar()

    if st.sidebar.button("Evaluate Business Impact"):
        results = score_customer(input_data)
        b = results["business"]

        arpu_value = b.get("ARPU", 0)
        ltv_value = b.get("LTV", round(arpu_value * 12, 2))

        
        # Executive Metrics — Revenue at Risk, ARPU, LTV, Potential Revenue Saved
    
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Executive Metrics</div>', unsafe_allow_html=True)

        left_big, right_metrics = st.columns([1.2, 1])

        # Main Metric — Revenue at Risk
        with left_big:
            st.markdown(f"""
            <div style="
                background-color:#FFFFFF;
                padding:28px;
                border-radius:12px;
                box-shadow:0px 2px 10px rgba(0,0,0,0.08);
                margin-bottom:18px;
                text-align:center;
            ">
                <div style="color:#6E6E6E; font-size:16px; margin-bottom:6px;">
                    Revenue at Risk
                </div>
                <div style="color:#2A4B8D; font-size:40px; font-weight:700;">
                    €{b['Revenue_at_Risk']:,}
                </div>
            </div>

            <details class="learn-more">
                <summary>Learn more ▾</summary>
                <div class="learn-more-panel">
                    <strong>Revenue at Risk</strong> estimates the monthly revenue that could be lost if the customer churns.<br><br>
                    It is calculated as:<br>
                    <code>ARPU × Churn Probability</code><br><br>
                    • ARPU comes from the customer's average monthly spend.<br>
                    • Churn Probability comes from the predictive model.<br><br>
                    This metric helps prioritize customers by financial impact.
                </div>
            </details>
            """, unsafe_allow_html=True)

        # Secondary Metrics — ARPU, LTV, Potential Revenue Saved
        with right_metrics:

            m1, m2 = st.columns(2)
            m3, m4 = st.columns(2)

            # Churn Probability
            with m1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Churn Probability</div>
                    <div class="kpi-value">{results['probability']:.2%}</div>
                </div>
                <details class="learn-more">
                    <summary>Learn more ▾</summary>
                    <div class="learn-more-panel">
                        <strong>Churn Probability</strong> is predicted by the churn model.<br><br>
                        It represents the likelihood that this customer will cancel their subscription in the near term.<br><br>
                        Higher probability → higher financial risk.
                    </div>
                </details>
                """, unsafe_allow_html=True)

            # ARPU
            with m2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">ARPU</div>
                    <div class="kpi-value">€{arpu_value}</div>
                </div>
                <details class="learn-more">
                    <summary>Learn more ▾</summary>
                    <div class="learn-more-panel">
                        <strong>ARPU (Average Revenue Per User)</strong> is the customer's average monthly spend.<br><br>
                        It comes directly from the input field <em>Avg Amount Paid</em>.<br><br>
                        ARPU helps quantify the customer's financial value.
                    </div>
                </details>
                """, unsafe_allow_html=True)

            # LTV
            with m3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">LTV (12‑month proxy)</div>
                    <div class="kpi-value">€{ltv_value}</div>
                </div>
                <details class="learn-more">
                    <summary>Learn more ▾</summary>
                    <div class="learn-more-panel">
                        <strong>LTV</strong> estimates the customer's projected 12‑month value.<br><br>
                        It is calculated as:<br>
                        <code>ARPU × 12</code><br><br>
                        If a more advanced LTV model is available, it will replace this proxy.
                    </div>
                </details>
                """, unsafe_allow_html=True)

            # Potential Revenue Saved
            with m4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Potential Revenue Saved</div>
                    <div class="kpi-value">€{b['Potential_Revenue_Saved']:,}</div>
                </div>
                <details class="learn-more">
                    <summary>Learn more ▾</summary>
                    <div class="learn-more-panel">
                        <strong>Potential Revenue Saved</strong> estimates how much revenue could be recovered with a retention action.<br><br>
                        It is calculated as:<br>
                        <code>30% × Revenue at Risk</code><br><br>
                        The 30% uplift is a benchmark used when no historical retention effectiveness data is available.
                    </div>
                </details>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Executive Narrative — Business Storytelling
    
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Executive Narrative</div>', unsafe_allow_html=True)

        st.markdown(f"""
<div style="color:#2A4B8D; font-size:16px; line-height:1.6;">
• This customer puts <strong>€{b['Revenue_at_Risk']:,}</strong> at risk.<br>
• Their churn probability is <strong>{results['probability']:.2%}</strong>, which explains the level of risk.<br>
• Their ARPU and LTV justify prioritizing this customer.<br>
• If we act, we can recover up to <strong>€{b['Potential_Revenue_Saved']:,}</strong>.
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    
        # Financial Visualizations (Placeholder)
        
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Financial Visualizations (Coming Soon)</div>', unsafe_allow_html=True)

        df = pd.DataFrame({
            "Revenue_at_Risk": [b['Revenue_at_Risk'] * x for x in [0.2, 0.5, 0.8, 1.0, 1.3, 1.6]],
            "Churn_Probability": [results["probability"] * x for x in [0.5, 0.8, 1.0, 1.2, 1.4, 1.6]],
            "LTV": [ltv_value * x for x in [0.6, 0.8, 1.0, 1.1, 1.3, 1.5]]
        })

        colA, colB = st.columns(2)

        # CHART 1
        with colA:
            st.markdown("<h3 style='color:#2A4B8D;'>Revenue at Risk Distribution</h3>", unsafe_allow_html=True)
            fig1 = px.histogram(df, x="Revenue_at_Risk", nbins=6, color_discrete_sequence=["#2A4B8D"])
            fig1.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=10, r=10, t=10, b=10),
                height=300,
                font=dict(color="#2A4B8D", size=13),
                xaxis=dict(
                    title_font=dict(color="#2A4B8D"),
                    tickfont=dict(color="#2A4B8D"),
                    gridcolor="#D9D9D9"
                ),
                yaxis=dict(
                    title_font=dict(color="#2A4B8D"),
                    tickfont=dict(color="#2A4B8D"),
                    gridcolor="#D9D9D9"
                ),
                hoverlabel=dict(
                    bgcolor="#F2F2F2",
                    font_size=12,
                    font_color="#2A4B8D"
                )
            )
            st.plotly_chart(fig1, use_container_width=True)

        # CHART 2
        with colB:
            st.markdown("<h3 style='color:#2A4B8D;'>LTV vs Churn Probability</h3>", unsafe_allow_html=True)
            fig2 = px.scatter(df, x="Churn_Probability", y="LTV", color_discrete_sequence=["#2A4B8D"])
            fig2.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=10, r=10, t=10, b=10),
                height=300,
                font=dict(color="#2A4B8D", size=13),
                xaxis=dict(
                    title_font=dict(color="#2A4B8D"),
                    tickfont=dict(color="#2A4B8D"),
                    gridcolor="#D9D9D9"
                ),
                yaxis=dict(
                    title_font=dict(color="#2A4B8D"),
                    tickfont=dict(color="#2A4B8D"),
                    gridcolor="#D9D9D9"
                ),
                hoverlabel=dict(
                    bgcolor="#F2F2F2",
                    font_size=12,
                    font_color="#2A4B8D"
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
<div style="
    background-color:#2A3B4D;
    color:white;
    padding:14px 18px;
    border-radius:8px;
    margin-top:18px;
    font-size:15px;
">
    Explore the Strategy & Actions layer to generate targeted retention interventions.
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)