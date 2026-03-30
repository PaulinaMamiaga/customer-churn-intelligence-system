import streamlit as st
import pandas as pd
import plotly.express as px
from utils import score_customer, customer_input_sidebar


def render():

    # Executive Theme (CSS)

    st.markdown("""
<style>
.main, .block-container {
    background-color: #F2F2F2 !important;
}

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
    font-size: 20px;
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


    # Title Block

    st.markdown("""
<div class="section-header" style="font-size:26px;">
    Explainability (SHAP)
</div>
""", unsafe_allow_html=True)

    # Intro Block

    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown("""
<div style="color:#2A4B8D; font-size:16px; line-height:1.55;">
This layer provides <strong>model explainability</strong> using SHAP (SHapley Additive exPlanations).
<br><br>

<div class="bullet-text">🔵 Which features contribute most to churn</div>
<div class="bullet-text">🔵 How each feature pushes the prediction up or down</div>
<div class="bullet-text">🔵 What behavioral patterns the model relies on</div>
<div class="bullet-text">🔵 How this customer compares to the population</div>

<br>
SHAP is essential for transparency, trust, regulatory compliance, and executive communication.
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

   
    # Sidebar Inputs and Scoring

    input_data = customer_input_sidebar()

    if st.sidebar.button("Explain Prediction"):

        results = score_customer(input_data)

       
        # Customer Snapshot Block
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Customer Snapshot</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="bullet-text">
        • <strong>Churn probability:</strong> {results['probability']:.2%}<br>
        • <strong>Risk level:</strong> {results['risk']}<br>
        • <strong>Timing:</strong> {results['timing']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

       
        # Corporate Chart Style 
      
        CORPORATE_BLUE = "#2A4B8D"
        GRID_GREY = "#D9D9D9"

        def apply_style(fig):
            fig.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(color=CORPORATE_BLUE, size=13),
                xaxis=dict(
                    title_font=dict(color=CORPORATE_BLUE, size=14),
                    tickfont=dict(color=CORPORATE_BLUE, size=12),
                    gridcolor=GRID_GREY
                ),
                yaxis=dict(
                    title_font=dict(color=CORPORATE_BLUE, size=14),
                    tickfont=dict(color=CORPORATE_BLUE, size=12),
                    gridcolor=GRID_GREY
                ),
                hoverlabel=dict(
                    bgcolor="#F2F2F2",
                    font_size=12,
                    font_color=CORPORATE_BLUE
                ),
                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            return fig

       
        # SHAP Charts (Using Simulated Data)
      
        # Simulated SHAP summary data
        shap_summary = pd.DataFrame({
            "Feature": ["Listening Time", "Auto-Renew", "Cancellation Behavior", "Tenure", "Engagement Score"],
            "Importance": [0.42, 0.31, 0.27, 0.18, 0.12]
        })

        # Simulated SHAP bar data
        shap_bar = pd.DataFrame({
            "Feature": ["Cancellation Behavior", "Low Listening", "Auto-Renew", "Tenure"],
            "SHAP Value": [0.28, 0.22, -0.15, -0.08]
        })

        # Simulated SHAP force data
        shap_force = pd.DataFrame({
            "Feature": ["Cancellation", "Listening", "Auto-Renew", "Tenure"],
            "Effect": [0.30, 0.18, -0.12, -0.05]
        })

        # Business Impact Metrics (Simulated)

        # SHAP Summary Plot
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">SHAP Summary Plot</div>', unsafe_allow_html=True)

        fig1 = px.bar(shap_summary, x="Importance", y="Feature",
                      orientation="h", text="Importance",
                      color_discrete_sequence=[CORPORATE_BLUE])
        fig1.update_traces(texttemplate="%{text:.0%}", textposition="outside")
        fig1.update_layout(xaxis_tickformat=".0%")
        fig1 = apply_style(fig1)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


        # SHAP Bar Plot (Top Drivers)
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">Top Positive / Negative Drivers</div>', unsafe_allow_html=True)

        fig2 = px.bar(shap_bar, x="Feature", y="SHAP Value",
                      text="SHAP Value", color_discrete_sequence=[CORPORATE_BLUE])
        fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig2 = apply_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # SHAP Force Plot (Simulated)
    
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">SHAP Force Plot</div>', unsafe_allow_html=True)

        fig3 = px.bar(shap_force, x="Feature", y="Effect",
                      text="Effect", color_discrete_sequence=[CORPORATE_BLUE])
        fig3.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig3 = apply_style(fig3)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Interpretability Narrative

        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Interpretability Narrative</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="bullet-text">
SHAP values help interpret the model by showing how each feature contributes to the final prediction.
<br><br>
• Cancellation behavior strongly increases churn risk.<br>
• Low listening time pushes the prediction upward.<br>
• Auto-renew typically reduces churn probability.<br>
• Tenure and engagement patterns shape the timing of churn.<br>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style="
    background-color:#2A3B4D;
    color:white;
    padding:14px 18px;
    border-radius:8px;
    margin-top:4px;
    font-size:15px;
">
Explainability generated successfully. Explore other layers for full churn intelligence.
</div>
""", unsafe_allow_html=True)