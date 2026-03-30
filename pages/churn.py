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

/* hide default marker */
.learn-more summary::-webkit-details-marker {
    display: none;
}

/* small panel for explanation */
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

    # Title + Explanation
   
    st.markdown("""
<div class="section-header" style="font-size:26px;">
    Churn Intelligence 
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown("""
<span style="color:#2A4B8D; font-size:16px; line-height:1.55;">

A complete executive view of **customer churn risk**, including:

  🔵 Probability of churn  
  🔵 Risk level  
  🔵 Key behavioral drivers  
  🔵 Expected churn timing  
  🔵 Behavioral patterns across customer segments  

</span>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Inputs
  
    input_data = customer_input_sidebar()

    if st.sidebar.button("Predict Churn"):
        results = score_customer(input_data)

        # Top Panel — Gauge + KPI Cards
    
        st.markdown('<div class="block">', unsafe_allow_html=True)
        top_left, top_right = st.columns([1.2, 1])

        # ----------------------------
        # Gauge Chart
        # ----------------------------
        with top_left:
            st.markdown('<div class="section-header">Churn Probability</div>', unsafe_allow_html=True)

            prob_value = results["probability"] * 100

            fig_gauge = {
                "data": [
                    {
                        "type": "indicator",
                        "mode": "gauge+number",
                        "value": prob_value,
                        "number": {"suffix": "%", "font": {"size": 38, "color": "#1A1A1A"}},
                        "gauge": {
                            "axis": {"range": [0, 100], "tickcolor": "#6E6E6E"},
                            "bar": {"color": "#2A4B8D"},
                            "steps": [
                                {"range": [0, 20], "color": "#E8F5E9"},
                                {"range": [20, 50], "color": "#FFF8E1"},
                                {"range": [50, 80], "color": "#FFE9D6"},
                                {"range": [80, 100], "color": "#FDECEA"},
                            ],
                            "threshold": {
                                "line": {"color": "#1A1A1A", "width": 3},
                                "thickness": 0.8,
                                "value": prob_value,
                            },
                        },
                    }
                ],
                "layout": {
                    "paper_bgcolor": "#F7F7F7",
                    "plot_bgcolor": "#F7F7F7",
                    "margin": {"t": 10, "b": 0, "l": 0, "r": 0},
                    "height": 260,
                },
            }

            st.plotly_chart(fig_gauge, use_container_width=True)

        # KPI Cards
        with top_right:
            st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)

            k1, k2 = st.columns(2)
            k3, k4 = st.columns(2)

            # Risk Level
            with k1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Risk Level</div>
                    <div class="kpi-value">{results['risk']}</div>
                </div>
                """, unsafe_allow_html=True)

            # ARPU
            with k2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">ARPU</div>
                    <div class="kpi-value">€{results['business']['ARPU']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Revenue at Risk
            with k3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Revenue at Risk</div>
                    <div class="kpi-value">€{results['business']['Revenue_at_Risk']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Potential Revenue Saved
            with k4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Potential Revenue Saved</div>
                    <div class="kpi-value">€{results['business']['Potential_Revenue_Saved']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Customer Insights + Behavioral Patterns
        
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Customer Insights</div>', unsafe_allow_html=True)

        question_color = "#2A4B8D"

        st.markdown(
            f"<p style='color:{question_color}; font-weight:700; font-size:18px;'>Why is this customer at risk?</p>",
            unsafe_allow_html=True
        )

        for item in results["drivers"]:
            st.markdown(
                f"<div style='color:{question_color}; font-size:16px;'>• {item}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"<p style='color:{question_color}; font-weight:700; font-size:18px;'>When is churn likely?</p>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div style='color:{question_color}; font-size:16px;'>• {results['timing']}</div>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # Behavioral Patterns (Unified Style)
    
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Behavioral Patterns</div>', unsafe_allow_html=True)

        colA, colB = st.columns(2)
        colC, colD = st.columns(2)

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

        # Chart 1
        with colA:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            df = pd.DataFrame({
                "listening_group": ["Low", "Medium-Low", "Medium-High", "High"],
                "churn_rate": [0.42, 0.31, 0.18, 0.07]
            })
            fig = px.bar(df, x="listening_group", y="churn_rate", text="churn_rate",
                         color_discrete_sequence=[CORPORATE_BLUE])
            fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig.update_layout(yaxis_tickformat=".0%")
            fig = apply_style(fig)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Chart 2
        with colB:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            df2 = pd.DataFrame({
                "auto_renew": ["Yes", "No"],
                "churn_rate": [0.12, 0.39]
            })
            fig2 = px.bar(df2, x="auto_renew", y="churn_rate", text="churn_rate",
                          color_discrete_sequence=[CORPORATE_BLUE])
            fig2.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig2.update_layout(yaxis_tickformat=".0%")
            fig2 = apply_style(fig2)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Chart 3
        with colC:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            df3 = pd.DataFrame({
                "cancelled_before": ["Yes", "No"],
                "churn_rate": [0.55, 0.18]
            })
            fig3 = px.bar(df3, x="cancelled_before", y="churn_rate", text="churn_rate",
                          color_discrete_sequence=[CORPORATE_BLUE])
            fig3.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig3.update_layout(yaxis_tickformat=".0%")
            fig3 = apply_style(fig3)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Chart 4
        with colD:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            df4 = pd.DataFrame({
                "tenure_bucket": ["0–6 months", "6–24 months", "24+ months"],
                "churn_rate": [0.48, 0.29, 0.12]
            })
            fig4 = px.bar(df4, x="tenure_bucket", y="churn_rate", text="churn_rate",
                          color_discrete_sequence=[CORPORATE_BLUE])
            fig4.update_traces(texttemplate="%{text:.0%}", textposition="outside")
            fig4.update_layout(yaxis_tickformat=".0%")
            fig4 = apply_style(fig4)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)