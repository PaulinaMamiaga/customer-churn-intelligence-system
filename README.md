# 🎧 KKBOX Retention Intelligence System  
### *AI‑powered churn prediction, explainability & business impact analytics*

The **KKBOX Retention Intelligence System** is an end‑to‑end analytics platform designed to help subscription businesses **understand, predict, and reduce customer churn**.  
It integrates **machine learning**, **explainability**, **forecasting**, **batch scoring**, and **executive‑level storytelling** into a single Streamlit application.

---

## 📌 Project Presentation  
**Canva Presentation:**  
👉 *(https://www.canva.com/design/DAHFzcQkZVw/RBnIQ95xY2t04xgIFafnxA/edit))*

---

## 🚀 Features

### 🔵 1. Churn Intelligence (Individual Prediction)
Customer‑level churn prediction enriched with:
- Churn probability  
- Risk level  
- Behavioral signals  
- Timing insights  
- Revenue at Risk  
- Personalized retention recommendations  

---

### 🔵 2. Business Impact (Executive Metrics)
Financial quantification for each customer:
- ARPU  
- LTV (12‑month proxy)  
- Revenue at Risk  
- Potential Revenue Saved  
- Auto‑generated executive narrative  

---

### 🔵 3. Batch Scoring (Large‑Scale Processing)
Upload a CSV/Excel file and score thousands of customers at once:
- Churn probability  
- Risk segmentation  
- Timing insights  
- Revenue at risk  
- Executive charts  
- CSV export  
- Executive PDF report  

Ideal for CRM teams and retention campaigns.

---

### 🔵 4. Prospective Forecast (Population‑Level Forecasting)
Upload a customer dataset to generate a 12‑month business forecast:
- Expected churners  
- Revenue at risk  
- Revenue saved  
- Base / Optimistic / Pessimistic scenarios  
- Executive insights for strategic planning  

---

### 🔵 5. Explainability (SHAP)
Full transparency of the model:
- Global feature importance  
- Positive/negative drivers  
- Stakeholder‑friendly interpretability  

---

### 🔵 6. Strategy & Actions
Actionable retention strategies based on:
- Risk level  
- Behavioral patterns  
- Financial impact  
- Customer segment  

---

## 🧱 Tech Stack

- Python 3.10+  
- Streamlit  
- scikit‑learn  
- Pandas / NumPy  
- Plotly  
- SHAP  
- FPDF2 / ReportLab  
- XGBoost  

---

## 📁 Project Structure
customer-churn-intelligence-system/
├── streamlit_app.py                # Main router
├── utils.py                        # Scoring + model loading
├── pdf_report.py                   # Executive PDF generator
│
├── app_pages/                      # All Streamlit pages
│   ├── home.py
│   ├── churn.py
│   ├── business.py
│   ├── strategy.py
│   ├── analytics.py
│   ├── shap_explain.py
│   ├── batch_scoring.py
│   └── prospective.py
│
├── model/
│   └── final_churn_model.pkl
│
├── data/
│   └── processed/df_clean.csv
│
└── README.md

---

## ▶️ How to Run

### 1. Install dependencies

### 2. Launch the application

### 3. Open in your browser

---

---

## 📊 Model Overview

- Binary classification (churn vs. non‑churn)  
- Features include:
  - Listening behavior  
  - Payment patterns  
  - Engagement  
  - Tenure  
  - Auto‑renewal  
  - Demographics  

The model outputs:
- Churn probability  
- Risk level  
- SHAP drivers  
- Timing insights  

---

## 🧠 Why This Project Matters

This system demonstrates your ability to build a **complete analytics product**, not just a model:

- Executive‑grade UI  
- Forecasting  
- Explainability  
- Batch processing  
- PDF reporting  
- Business storytelling  
- Modular architecture  

It is a **portfolio‑ready, product‑level project** that showcases technical depth and strategic thinking.

---

## 📌 Future Enhancements

- Cohort‑based retention forecasting  
- Advanced LTV modeling  
- Real‑time scoring API  
- CRM integration  
- SHAP integration in batch scoring  