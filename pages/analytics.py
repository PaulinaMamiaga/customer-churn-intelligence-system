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
    Segment Analytics
</div>
""", unsafe_allow_html=True)

    # Intro Block
    
    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown("""
<div style="color:#2A4B8D; font-size:16px; line-height:1.55;">
This layer provides <strong>population-level churn analytics</strong>, helping you understand where churn concentrates and which customer groups are most vulnerable.
<br><br>

<div class="bullet-text">🔵 Churn concentration across segments</div>
<div class="bullet-text">🔵 Behavioral patterns linked to churn</div>
<div class="bullet-text">🔵 Subscription attributes driving risk</div>
<div class="bullet-text">🔵 Segment-level vulnerability insights</div>

</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    
    # Sidebar Input + Analyze Button
   
    input_data = customer_input_sidebar()

    if st.sidebar.button("Analyze Segments"):

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

        # Segment Analytics Block
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Churn Across Key Segments</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="bullet-text">
These charts help identify <strong>where churn happens</strong> across the customer base and which segments show the highest vulnerability.
</div>
""", unsafe_allow_html=True)

        
        # Corporate color scheme for charts
      
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

        
        # Chart DataFrames (Example Data)
       
        churn_by_listening = pd.DataFrame({
            "Listening Group": ["Low", "Medium-Low", "Medium", "High"],
            "Churn Rate": [0.32, 0.21, 0.12, 0.05]
        })

        churn_by_autorenew = pd.DataFrame({
            "Auto-Renew": ["Off", "On"],
            "Churn Rate": [0.28, 0.09]
        })

        churn_by_cancel = pd.DataFrame({
            "Cancellation Behavior": ["Cancelled Before", "Never Cancelled"],
            "Churn Rate": [0.41, 0.11]
        })

        churn_by_tenure = pd.DataFrame({
            "Tenure Bucket": ["0–3 months", "3–6 months", "6–12 months", "12+ months"],
            "Churn Rate": [0.37, 0.22, 0.14, 0.07]
        })

        churn_by_payment = pd.DataFrame({
            "Payment Variability": ["High", "Medium", "Low"],
            "Churn Rate": [0.33, 0.18, 0.09]
        })

        churn_by_city = pd.DataFrame({
            "City Group": ["Tier 3", "Tier 2", "Tier 1"],
            "Churn Rate": [0.29, 0.17, 0.08]
        })

        
        # Charts

        colA, colB = st.columns(2)

        with colA:
            st.markdown('<div class="subsection-title">Churn by Listening Group</div>', unsafe_allow_html=True)
            fig = px.bar(churn_by_listening, x="Listening Group", y="Churn Rate",
                         text="Churn Rate", color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)

        with colB:
            st.markdown('<div class="subsection-title">Churn by Auto-Renew</div>', unsafe_allow_html=True)
            fig = px.bar(churn_by_autorenew, x="Auto-Renew", y="Churn Rate",
                         text="Churn Rate", color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)

        colC, colD = st.columns(2)

        with colC:
            st.markdown('<div class="subsection-title">Churn by Cancellation Behavior</div>', unsafe_allow_html=True)
            fig = px.bar(churn_by_cancel, x="Cancellation Behavior", y="Churn Rate",
                         text="Churn Rate", color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)

        with colD:
            st.markdown('<div class="subsection-title">Churn by Tenure Buckets</div>', unsafe_allow_html=True)
            fig = px.bar(churn_by_tenure, x="Tenure Bucket", y="Churn Rate",
                         text="Churn Rate", color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)

        colE, colF = st.columns(2)

        with colE:
            st.markdown('<div class="subsection-title">Churn by Payment Variability</div>', unsafe_allow_html=True)
            fig = px.bar(churn_by_payment, x="Payment Variability", y="Churn Rate",
                         text="Churn Rate", color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)

        with colF:
            st.markdown('<div class="subsection-title">Churn by City Group</div>', unsafe_allow_html=True)
            fig = px.bar(churn_by_city, x="City Group", y="Churn Rate",
                         text="Churn Rate", color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

       
        # Insights Summary Block
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Insights Summary</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="bullet-text">
Segment-level analytics reveal <strong>high-risk customer groups</strong> and guide targeted retention strategies.
<br><br>
• Low-engagement listening groups typically show higher churn.<br>
• Customers without auto-renew often churn earlier.<br>
• Cancellation behavior is one of the strongest churn predictors.<br>
• Tenure buckets reveal early-stage vs late-stage churn patterns.<br>
• Payment variability can indicate unstable subscription behavior.<br>
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
Explore the SHAP Explainability layer to understand model-level drivers.
</div>
""", unsafe_allow_html=True)