import streamlit as st
from utils import score_customer, customer_input_sidebar
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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

/* Subsection titles */
.subsection-title {
    color: #2A4B8D;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* Bullet text */
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
    Strategy & Actions
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown("""
<div style="color:#2A4B8D; font-size:16px; line-height:1.55;">
This layer transforms churn insights into <strong>concrete, actionable retention strategies</strong>.
It combines:
<br><br>

<div class="bullet-text">🔵 Risk assessment</div>
<div class="bullet-text">🔵 Behavioral drivers</div>
<div class="bullet-text">🔵 Timing intelligence</div>
<div class="bullet-text">🔵 Business impact</div>
<div class="bullet-text">🔵 Recommended interventions</div>

</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    
    # Inputs and Scoring
   
    input_data = customer_input_sidebar()

    if st.sidebar.button("Generate Strategy"):
        results = score_customer(input_data)
        b = results["business"]

        ARPU = b.get("ARPU", 0)
        LTV = b.get("LTV", None)
        RISK_REV = b.get("Revenue_at_Risk", 0)
        SAVED_REV = b.get("Potential_Revenue_Saved", 0)

        
        # Risk & Context Panel
        
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Risk & Context</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1.1, 1])

        with col_left:
            st.markdown('<div class="subsection-title">Risk Snapshot</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="bullet-text">
                • <strong>Churn probability:</strong> {results['probability']:.2%}<br>
                • <strong>Risk level:</strong> {results['risk']}<br>
                • <strong>Timing:</strong> {results['timing']}
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="subsection-title">Key Drivers</div>', unsafe_allow_html=True)
            if results["drivers"]:
                for d in results["drivers"]:
                    st.markdown(f"<div class='bullet-text'>• {d}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='bullet-text'>• No dominant drivers detected.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        
        # Recommended Strategic Actions
        
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Recommended Strategic Actions</div>', unsafe_allow_html=True)

        suggestions = []

        if results["risk"] in ["High", "Extreme"]:
            suggestions.append("Deploy a win‑back or save‑offer within the next 7–14 days.")

        if input_data["has_cancelled"] == 1:
            suggestions.append("Send a recovery campaign acknowledging the cancellation and offering a tailored plan.")

        if input_data["total_secs"] < 30_000:
            suggestions.append("Launch a re‑engagement journey: curated playlists, personalized recommendations, and usage nudges.")

        if input_data["has_auto_renew"] == 0:
            suggestions.append("Promote auto‑renew with a small incentive to increase commitment.")

        if input_data["listening_group"] in ["Low", "Medium-Low"]:
            suggestions.append("Offer personalized content bundles to increase listening frequency.")

        if not suggestions:
            suggestions.append("Monitor this customer and include them in light‑touch engagement campaigns.")

        st.markdown('<div class="subsection-title">Action Playbook</div>', unsafe_allow_html=True)

        for s in suggestions:
            st.markdown(f"<div class='bullet-text'>• {s}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        
        # AI‑Generated Strategy (Updated For OPENAI v1+)
        
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">AI‑Generated Strategy</div>', unsafe_allow_html=True)

        LTV_display = LTV if LTV is not None else "N/A"

        prompt = f"""
Act as a senior strategy consultant specializing in subscription-based digital products.
Provide an executive retention strategy based on:

Segment: {input_data.get('segment', 'N/A')}
Churn risk: {results['risk']}
Behavior: {", ".join(results['drivers'])}
CLV: {LTV_display}
Usage: {input_data.get('total_secs', 'N/A')}
Interactions: {results['timing']}

Return the output in EXACTLY the following format.
Do not change labels, punctuation, spacing, or markdown style.

**Diagnosis:** <1–2 sentences>

**Opportunity:** <1 sentence>

**Actions:**
1. <action 1>
2. <action 2>
3. <action 3>

**Customer message:** <1 sentence>

Rules:
- The labels MUST appear exactly as written above.
- The labels MUST be bold (surrounded by **).
- Each action MUST be on its own line and MUST start with "1.", "2.", "3.".
- Do NOT merge actions into a single paragraph.
- Do NOT add extra headings, commentary, or sections.
- Do NOT reorder anything.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.4
            )

            ai_strategy = response.choices[0].message.content

            st.markdown(f"""
            <div style="
                background-color:#F2F2F2;
                color:#2A4B8D;
                padding:14px 16px;
                border-radius:8px;
                font-size:14px;
                line-height:1.6;
            ">
            {ai_strategy}
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error("⚠️ There was an issue generating the AI strategy.")
            st.caption(str(e))

        st.markdown("</div>", unsafe_allow_html=True)

    
        # Executive Closing Block
        
        st.markdown("""
<div style="
    background-color:#2A3B4D;
    color:white;
    padding:14px 18px;
    border-radius:8px;
    margin-top:4px;
    font-size:15px;
">
    Strategy generated successfully. Explore the other layers to align risk, impact, and actions into a unified retention plan.
</div>
""", unsafe_allow_html=True)