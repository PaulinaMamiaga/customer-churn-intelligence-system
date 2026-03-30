# utils.py
import streamlit as st
import pandas as pd
import pickle

# 1. Load Model
@st.cache_resource
def load_model():
    with open("model/final_churn_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# 2. Core Scoring Function
def score_customer(input_dict: dict):
    """Returns churn probability, risk, business metrics, drivers, timing."""
    df = pd.DataFrame([input_dict])
    prob = float(model.predict_proba(df)[0, 1])

    # Risk label
    if prob < 0.2:
        risk = "Low"
    elif prob < 0.5:
        risk = "Medium"
    elif prob < 0.8:
        risk = "High"
    else:
        risk = "Extreme"

    # Business layer (monthly logic)
    arpu = float(input_dict["avg_amount_paid"])  # monthly average revenue per user
    revenue_at_risk = prob * arpu                # monthly revenue at risk
    potential_saved = 0.3 * revenue_at_risk      # example: 30% retention lift

    business = {
        "ARPU": round(arpu, 2),
        "Revenue_at_Risk": round(revenue_at_risk, 2),
        "Potential_Revenue_Saved": round(potential_saved, 2),
    }

    # Drivers
    drivers = []
    if input_dict["has_cancelled"] == 1:
        drivers.append("Customer has cancelled at least once.")
    if input_dict["has_auto_renew"] == 0:
        drivers.append("Customer is not on auto-renew (low commitment).")
    if input_dict["total_secs"] < 30_000:
        drivers.append("Low listening time (weak engagement).")
    if input_dict["listening_group"] in ["Low", "Medium-Low"]:
        drivers.append("Customer belongs to a low engagement listening group.")
    if not drivers:
        drivers.append("No strong red flags detected; monitor engagement and payment behavior.")

    # Timing
    if input_dict["customer_tenure_days"] < 180:
        timing = "Early-stage churn risk (first 6 months)."
    elif input_dict["customer_tenure_days"] < 730:
        timing = "Mid-lifecycle risk; next 3–6 months are critical."
    else:
        timing = "Late-stage churn risk; risk of silent disengagement in the next 1–3 months."

    return {
        "probability": prob,
        "risk": risk,
        "business": business,
        "drivers": drivers,
        "timing": timing,
    }

# 3. Sidebar Inputs
def customer_input_sidebar():
    st.sidebar.subheader("Customer Input")

    gender = st.sidebar.selectbox("Gender", ["male", "female", "unknown"])
    age = st.sidebar.slider("Age", 0, 100, 28)

    city = st.sidebar.selectbox("City Grouped", ["1","2","3","4","5","other"], index=4)
    via = st.sidebar.selectbox("Registered Via", ["3","7","9","13","other"], index=0)

    listening_group = st.sidebar.selectbox(
        "Listening Group",
        ["Low", "Medium-Low", "Medium-High", "High"],
        index=1
    )

    has_auto_renew = st.sidebar.selectbox("Auto-Renew", [0, 1], index=1)
    has_cancelled = st.sidebar.selectbox("Cancelled", [0, 1], index=0)

    avg_paid = st.sidebar.slider("Avg Amount Paid", 0, 2000, 120)
    total_paid = st.sidebar.slider("Total Amount Paid", 0, 20000, 600)

    secs = st.sidebar.slider("Total Listening Seconds", 0, 2_000_000, 50_000)
    unq = st.sidebar.slider("Unique Songs", 0, 20000, 200)

    tenure = st.sidebar.slider("Customer Tenure (days)", 0, 5000, 800)
    variability = st.sidebar.slider("Payment Variability", 0, 500, 20)

    return {
        "gender": gender,
        "age": age,
        "city_grouped": city,
        "registered_via_grouped": via,
        "avg_amount_paid": avg_paid,
        "total_amount_paid": total_paid,
        "has_auto_renew": has_auto_renew,
        "has_cancelled": has_cancelled,
        "total_secs": secs,
        "num_unq": unq,
        "customer_tenure_days": tenure,
        "listening_group": listening_group,
        "payment_variability": variability
    }