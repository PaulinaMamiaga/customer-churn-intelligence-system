import streamlit as st
import pandas as pd
import plotly.express as px
import time
from utils import score_customer
from pdf_report import generate_pdf_report   # <-- PDF integration

# Batch Scoring Module

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

/* Force Streamlit error text to be black */
.stAlert div {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

    
    # Title Block
    
    st.markdown("""
<div class="section-header" style="font-size:26px;">
    Batch Customer Scoring
</div>
""", unsafe_allow_html=True)

    
    # Intro Block
    
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown("""
<div class="bullet-text" style="font-size:16px;">
Upload a dataset of customers to generate churn predictions at scale.
This module enriches your dataset with:
<br><br>
🔵 Churn probability<br>
🔵 Risk level<br>
🔵 Timing insights<br>
🔵 Revenue at risk<br>
🔵 Drivers (optional)<br><br>
Ideal for retention campaigns, prioritization, and executive reporting.
</div>
""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    
    # File Upload and Validation
    
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">Upload Customer Dataset (CSV or Excel)</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Customer Dataset", type=["csv", "xlsx"])

    st.markdown(
        """
        <p style='font-size:13px; color:#2A4B8D; margin-top:5px;'>
        Required columns for batch scoring:<br>
        <b>total_secs</b>, <b>has_auto_renew</b>, <b>has_cancelled</b>, 
        <b>customer_tenure_days</b>, <b>city_grouped</b>, <b>payment_variability</b>,<br>
        <b>avg_amount_paid</b>, <b>total_amount_paid</b>, <b>num_unq</b>,
        <b>gender</b>, <b>age</b>, <b>registered_via_grouped</b>, <b>listening_group</b>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:

        
        # Load Dataset with Timing
        
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Loading Dataset</div>', unsafe_allow_html=True)

        load_start = time.time()
        df = pd.read_csv(uploaded_file)
        load_elapsed = time.time() - load_start

        st.markdown(
            f"<div class='bullet-text'>Dataset loaded in <b>{load_elapsed:.2f} seconds</b>. "
            f"Rows: <b>{len(df):,}</b></div>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        
        # Validation of Required Columns

        required_cols = [
            "total_secs", "has_auto_renew", "has_cancelled",
            "customer_tenure_days", "city_grouped", "payment_variability",
            "avg_amount_paid", "total_amount_paid", "num_unq",
            "gender", "age", "registered_via_grouped", "listening_group"
        ]

        missing = [c for c in required_cols if c not in df.columns]

        if missing:
            st.error(f"Missing required columns: {missing}")
            return

        
        # Scoring + ETA
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Processing Customers</div>', unsafe_allow_html=True)

        progress = st.progress(0)
        results = []

        start_time = time.time()
        eta_placeholder = st.empty()

        for i, row in df.iterrows():
            result = score_customer(row.to_dict())
            results.append(result)

            progress.progress((i + 1) / len(df))

            elapsed = time.time() - start_time
            avg_time_per_row = elapsed / (i + 1)
            remaining_rows = len(df) - (i + 1)
            eta_seconds = remaining_rows * avg_time_per_row
            eta_min = int(eta_seconds // 60)
            eta_sec = int(eta_seconds % 60)

            time.sleep(0.001)

            eta_placeholder.markdown(
                f"""
                <div style='font-size:15px; color:#2A4B8D; margin-top:10px;'>
                    Processed <b>{i+1:,}</b> of <b>{len(df):,}</b> customers<br>
                    Elapsed: <b>{elapsed:.1f}s</b><br>
                    Estimated time remaining: <b>{eta_min}m {eta_sec}s</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        scoring_elapsed = time.time() - start_time

        scored_df = df.copy()
        scored_df["churn_probability"] = [r["probability"] for r in results]
        scored_df["risk_level"] = [r["risk"] for r in results]
        scored_df["timing"] = [r["timing"] for r in results]

        st.success(f"Batch scoring completed successfully in {scoring_elapsed:.2f} seconds.")

        st.markdown("</div>", unsafe_allow_html=True)

        
        # Results Table + Download
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Scored Dataset</div>', unsafe_allow_html=True)

        st.dataframe(scored_df, use_container_width=True)

        st.download_button(
            label="Download Scored CSV",
            data=scored_df.to_csv(index=False),
            file_name="scored_customers.csv",
            mime="text/csv"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        
        # Summary charts 
    
        CORPORATE_BLUE = "#2A4B8D"
        GRID_GREY = "#D9D9D9"

        def apply_style(fig):
            fig.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(color=CORPORATE_BLUE, size=13),

                xaxis=dict(
                    gridcolor=GRID_GREY,
                    tickfont=dict(color=CORPORATE_BLUE),
                    title=dict(font=dict(color=CORPORATE_BLUE))
                ),
                yaxis=dict(
                    gridcolor=GRID_GREY,
                    tickfont=dict(color=CORPORATE_BLUE),
                    title=dict(font=dict(color=CORPORATE_BLUE))
                ),

                legend=dict(
                    font=dict(color=CORPORATE_BLUE)
                ),

                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            return fig

       
        # Chart 1 — Risk Distribution
       
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">Risk Level Distribution</div>', unsafe_allow_html=True)

        fig1 = px.histogram(scored_df, x="risk_level", color="risk_level",
                            color_discrete_sequence=[CORPORATE_BLUE])
        fig1 = apply_style(fig1)
        st.plotly_chart(fig1, use_container_width=True, key="risk_summary")

        # Chart 2 — Churn Probability Distribution
      
        st.markdown('<div class="subsection-title">Churn Probability Distribution</div>', unsafe_allow_html=True)

        fig2 = px.histogram(scored_df, x="churn_probability",
                            color_discrete_sequence=[CORPORATE_BLUE])
        fig2.update_layout(xaxis_tickformat=".0%")
        fig2 = apply_style(fig2)
        st.plotly_chart(fig2, use_container_width=True, key="prob_summary")

        st.markdown("</div>", unsafe_allow_html=True)

        # Executive Summary + Narrative
      
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Executive Report</div>', unsafe_allow_html=True)

        avg_churn = scored_df["churn_probability"].mean()
        high_risk = (scored_df["risk_level"] == "High").sum()
        extreme_risk = (scored_df["risk_level"] == "Extreme").sum()
        revenue_at_risk = (scored_df["churn_probability"] * scored_df["total_secs"]).sum()

        st.markdown('<div class="subsection-title">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="bullet-text">
<b>Average churn probability:</b> {avg_churn:.2%}<br>
<b>High-risk customers:</b> {high_risk:,}<br>
<b>Extreme-risk customers:</b> {extreme_risk:,}<br>
<b>Total Revenue at Risk:</b> €{revenue_at_risk:,.0f}<br>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="subsection-title">Churn Intelligence</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, key="prob_exec")

        st.markdown('<div class="subsection-title">Business Impact</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="bullet-text">
Retention efforts focused on high and extreme risk customers could reduce churn by up to 
<b>{(high_risk + extreme_risk) / len(scored_df):.2%}</b> and protect significant revenue.
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="subsection-title">Strategy & Actions</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="bullet-text">
• Prioritize outreach to high and extreme risk segments.<br>
• Offer targeted incentives to medium-risk customers.<br>
• Reinforce engagement for low-risk customers to maintain loyalty.<br>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="subsection-title">Segment Analytics</div>', unsafe_allow_html=True)
        seg_fig = px.box(scored_df, x="listening_group", y="churn_probability",
                         color_discrete_sequence=[CORPORATE_BLUE])
        seg_fig = apply_style(seg_fig)
        st.plotly_chart(seg_fig, use_container_width=True, key="segment_exec")

        st.markdown('<div class="subsection-title">Explainability (SHAP)</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="bullet-text">
Explainability is available in the dedicated Explainability (SHAP) module. 
Future versions can integrate SHAP summaries directly into this batch report.
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        
        # Executive PDF Report for Download
    
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Download Executive PDF Report</div>', unsafe_allow_html=True)

        st.markdown(
            "<div class='bullet-text'>Download a full executive report including risk distribution, "
            "probability analysis, and behavioral signals.</div>",
            unsafe_allow_html=True
        )

        figs_dict = {
            "risk_distribution": fig1,
            "probability_distribution": fig2
        }

        if st.button("Download Executive PDF Report"):
            pdf_path = generate_pdf_report(
                customer_id="Batch Summary",
                probability=scored_df["churn_probability"].mean(),
                risk="N/A (Batch Summary)",
                business={
                    "Revenue_at_Risk": scored_df["churn_probability"].mean() * scored_df["total_secs"].mean(),
                    "Potential_Revenue_Saved": scored_df["churn_probability"].mean() * scored_df["total_secs"].mean() * 0.3
                },
                drivers=["Aggregated batch-level insights"],
                timing="Batch-level summary (no individual timing).",
                figs_dict=figs_dict
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Executive PDF Report",
                    data=f,
                    file_name="executive_report.pdf",
                    mime="application/pdf"
                )

        st.markdown("</div>", unsafe_allow_html=True)