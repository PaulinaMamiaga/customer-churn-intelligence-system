import streamlit as st


# 1. Global Setup
st.set_page_config(
    page_title="KKBOX Retention Intelligence System",
    page_icon="🎧",
    layout="wide"
)


# 2. Sidebar Navigation

# Title And Branding
st.sidebar.markdown(
    "<h2 style='color:white; margin-bottom:10px;'>🎧 KKBOX Retention OS</h2>",
    unsafe_allow_html=True
)

# Navigation Label 
st.sidebar.markdown(
    "<p style='color:white; font-size:14px; font-weight:600;'>Navigate</p>",
    unsafe_allow_html=True
)

# Menu Options
page = st.sidebar.radio(
    "",
    [
        "⌂ Home",
        "Churn Intelligence",
        "Business Impact",
        "Strategy & Actions",
        "Segment Analytics",
        "Explainability (SHAP)",
        "Batch Scoring"
    ]
)

# 3. Page Router
if page == "⌂ Home":
    import pages.home as home
    home.render()

elif page == "Churn Intelligence":
    import pages.churn as churn
    churn.render()

elif page == "Business Impact":
    import pages.business as business
    business.render()

elif page == "Strategy & Actions":
    import pages.strategy as strategy
    strategy.render()

elif page == "Segment Analytics":
    import pages.analytics as analytics
    analytics.render()

elif page == "Explainability (SHAP)":
    import pages.shap_explain as shap_explain
    shap_explain.render()

elif page == "Batch Scoring":
    import pages.batch_scoring as batch_scoring
    batch_scoring.render()