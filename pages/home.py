import streamlit as st

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
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 18px;
}

.subsection-title {
    color: #2A4B8D;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.bullet-text {
    color: #2A4B8D;
    font-size: 15px;
    line-height: 1.55;
}
</style>
""", unsafe_allow_html=True)

    # Title Block
    st.markdown("""
<div class="section-header">
    🎧 KKBOX Retention Intelligence System
</div>
""", unsafe_allow_html=True)

   
    # Intro Block
    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown("""
<div class="bullet-text" style="font-size:16px;">
Welcome to the <strong>KKBOX Retention Intelligence System</strong>, a modern platform designed to help you
understand, predict, and prevent customer churn with clarity and precision.
<br><br>

This system combines:
<br><br>
🔵 <strong>Predictive modeling</strong> — Who will churn<br>
🔵 <strong>Explainability</strong> — Why they churn<br>
🔵 <strong>Timing intelligence</strong> — When churn is likely<br>
🔵 <strong>Business impact analysis</strong> — How much revenue is at risk<br>
🔵 <strong>Strategic recommendations</strong> — What actions to take<br>
🔵 <strong>Segment analytics</strong> — Where churn concentrates across the base<br>
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    
    # What You Can Do Block

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">What You Can Do Here</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="subsection-title">Churn Intelligence</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="bullet-text">
        Predict churn, understand risk levels, and explore why and when churn happens.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="subsection-title">Business Impact</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="bullet-text">
        Quantify ARPU, LTV, revenue at risk, and financial implications of churn.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="subsection-title">Strategy & Actions</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="bullet-text">
        Generate actionable retention strategies and personalized interventions.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

  
    # Aadvanced Analytics Block

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Advanced Analytics</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="bullet-text">
Explore churn patterns across customer segments, behaviors, and subscription attributes.
Dive into explainability with SHAP to understand the model's decision-making.
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    
    # Footer Block
    st.markdown("""
<div style="
    background-color:#2A3B4D;
    color:white;
    padding:14px 18px;
    border-radius:8px;
    margin-top:4px;
    font-size:15px;
">
Use the left sidebar to navigate through the different intelligence layers.
</div>
""", unsafe_allow_html=True)