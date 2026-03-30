import os
import tempfile
from datetime import datetime

import plotly.io as pio
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)

# Export Plotly Figures To PNG (Kaleido Backend)
def save_plotly_image(fig):
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    pio.write_image(fig, tmpfile.name, format="png", scale=2)
    return tmpfile.name


# Generate PDF (ReportLab — Landscape Dashboard Style)

def generate_pdf_report(customer_id, probability, risk, business, drivers, timing, figs_dict):
    # Export figures we receive
    img_paths = {}
    for key, fig in figs_dict.items():
        img_paths[key] = save_plotly_image(fig)

    # PDF path
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = tmp_pdf.name

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=28,
        textColor=colors.white,
        alignment=1,
        spaceAfter=20,
    )
    section_title = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=20,
        textColor=colors.HexColor("#2A4B8D"),
        spaceAfter=12,
    )
    normal = ParagraphStyle(
        "NormalBlue",
        parent=styles["BodyText"],
        textColor=colors.HexColor("#2A4B8D"),
        fontSize=11,
        leading=14,
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        textColor=colors.HexColor("#555555"),
        fontSize=9,
        leading=11,
    )

    # Document (A4 landscape)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    story = []

    # Cover Page (Simulated Gradient + Logo)

    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=5 * cm, height=5 * cm))
        story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("<b>KKBOX Retention Intelligence Report</b>", title_style))
    story.append(Paragraph("Batch Scoring — Executive Dashboard View", normal))
    story.append(Paragraph(datetime.today().strftime("%B %d, %Y"), normal))
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph(f"Customer ID: <b>{customer_id}</b>", normal))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Made by <b>KKBOX Retention OS</b>", small))
    story.append(Spacer(1, 2 * cm))

    # Table Of Contents (Manual Index)

    story.append(Paragraph("Index", section_title))
    toc_items = [
        "1. Executive KPI Summary",
        "2. Risk & Churn Distributions",
        "3. Advanced Segmentation Insights",
        "4. Personalized Recommendations",
        "5. Revenue Forecasting",
        "6. Explainability (SHAP)",
        "7. Cohort Retention",
        "8. Risk Heatmap",
        "9. Correlation Analysis",
        "10. Tenure Retention",
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", normal))
    story.append(Spacer(1, 1 * cm))

    # Executive KPI Table

    story.append(Paragraph("1. Executive KPI Summary", section_title))

    kpi_data = [
        ["Metric", "Value"],
        ["Churn Probability", f"{probability:.2%}"],
        ["Risk Level", risk],
        ["Revenue at Risk", f"€{business['Revenue_at_Risk']:,.0f}"],
        ["Potential Revenue Saved", f"€{business['Potential_Revenue_Saved']:,.0f}"],
        ["Timing Insights", timing],
    ]

    kpi_table = Table(kpi_data, colWidths=[8 * cm, 10 * cm])
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2A4B8D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ]
        )
    )

    story.append(kpi_table)
    story.append(Spacer(1, 0.8 * cm))


    # Risk & Churn Distributions

    story.append(Paragraph("2. Risk & Churn Distributions", section_title))

    if "risk_distribution" in img_paths:
        story.append(Paragraph("Risk Level Distribution", normal))
        story.append(Image(img_paths["risk_distribution"], width=10 * cm, height=6 * cm))
        story.append(Spacer(1, 0.5 * cm))

    if "probability_distribution" in img_paths:
        story.append(Paragraph("Churn Probability Distribution", normal))
        story.append(Image(img_paths["probability_distribution"], width=10 * cm, height=6 * cm))
        story.append(Spacer(1, 0.8 * cm))


    # Advanced Segmentation Insights

    story.append(Paragraph("3. Advanced Segmentation Insights", section_title))
    story.append(
        Paragraph(
            """
        This section highlights how churn probability varies across key customer segments.
        Use these insights to prioritize retention actions and personalize interventions.
        """,
            normal,
        )
    )

    segmentation_points = [
        "Listening Behavior: Identify segments with low engagement patterns.",
        "Registration Channel: Channels with higher churn risk may require onboarding improvements.",
        "City Group: Regional churn patterns can reveal market-specific issues.",
        "Age Group: Younger or older cohorts may show distinct churn behaviors.",
    ]
    for p in segmentation_points:
        story.append(Paragraph(f"• {p}", normal))
    story.append(Spacer(1, 0.8 * cm))

    
    # Personalized Recommendations

    story.append(Paragraph("4. Personalized Recommendations", section_title))

    recs = [
        "Target high-risk users with personalized retention campaigns.",
        "Offer incentives to medium-risk users to reinforce engagement.",
        "Improve onboarding flows for segments with high early churn.",
        "Deploy push notifications for users with declining activity.",
        "Promote premium features to users with high lifetime value.",
    ]
    for r in recs:
        story.append(Paragraph(f"• {r}", normal))
    story.append(Spacer(1, 0.8 * cm))


    # Revenue Forecasting

    story.append(Paragraph("5. Revenue Forecasting", section_title))

    projected_loss = business["Revenue_at_Risk"] * 1.15
    projected_saved = business["Potential_Revenue_Saved"] * 1.25

    story.append(
        Paragraph(f"<b>Projected Revenue Loss:</b> €{projected_loss:,.0f}", normal)
    )
    story.append(
        Paragraph(f"<b>Projected Revenue Saved:</b> €{projected_saved:,.0f}", normal)
    )
    story.append(Spacer(1, 0.8 * cm))


    # SHAP Section 

    story.append(Paragraph("6. Explainability (SHAP)", section_title))
    story.append(
        Paragraph(
            """
        SHAP values provide transparency into the model’s decision-making process.
        They highlight which features most strongly influence churn predictions.
        High SHAP value → strong positive contribution to churn risk.
        Negative SHAP value → reduces churn risk.
        """,
            normal,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    if "shap_summary" in img_paths:
        story.append(Paragraph("SHAP Summary Plot", normal))
        story.append(Image(img_paths["shap_summary"], width=12 * cm, height=7 * cm))
        story.append(Spacer(1, 0.5 * cm))

    if "shap_bar" in img_paths:
        story.append(Paragraph("Top Features by SHAP Impact", normal))
        story.append(Image(img_paths["shap_bar"], width=12 * cm, height=7 * cm))
        story.append(Spacer(1, 0.8 * cm))


    # Cohort Retention
    

    story.append(Paragraph("7. Cohort Retention", section_title))
    story.append(
        Paragraph(
            """
        Cohort-based retention curves show how different signup cohorts retain over time.
        This helps identify structural issues in onboarding, product-market fit, or pricing.
        """,
            normal,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    if "cohort_retention" in img_paths:
        story.append(Image(img_paths["cohort_retention"], width=12 * cm, height=7 * cm))
        story.append(Spacer(1, 0.8 * cm))


    # Risk Heatmap

    story.append(Paragraph("8. Risk Heatmap", section_title))
    story.append(
        Paragraph(
            """
        The risk heatmap highlights combinations of key dimensions (e.g., city, tenure, engagement)
        where churn risk is concentrated. Use this to focus retention resources where they matter most.
        """,
            normal,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    if "risk_heatmap" in img_paths:
        story.append(Image(img_paths["risk_heatmap"], width=12 * cm, height=7 * cm))
        story.append(Spacer(1, 0.8 * cm))


    # Correlation Analysis

    story.append(Paragraph("9. Correlation Analysis", section_title))
    story.append(
        Paragraph(
            """
        Correlation analysis reveals how behavioral and financial features move together.
        This can surface hidden drivers of churn and inform feature engineering and product strategy.
        """,
            normal,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    if "correlation_matrix" in img_paths:
        story.append(Image(img_paths["correlation_matrix"], width=12 * cm, height=7 * cm))
        story.append(Spacer(1, 0.8 * cm))


    # Tenure Retention

    story.append(Paragraph("10. Tenure Retention", section_title))
    story.append(
        Paragraph(
            """
        Retention by tenure shows how long customers stay before churning.
        This helps identify critical windows where proactive engagement can have the highest impact.
        """,
            normal,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    if "tenure_retention" in img_paths:
        story.append(Image(img_paths["tenure_retention"], width=12 * cm, height=7 * cm))
        story.append(Spacer(1, 0.8 * cm))

    
    # Signature

    story.append(Spacer(1, 1 * cm))
    story.append(
        Paragraph(
            "Made by <b>KKBOX Retention OS</b>",
            small,
        )
    )

    # Build PDF
    doc.build(story)

    # Cleanup images
    for p in img_paths.values():
        os.remove(p)

    return pdf_path