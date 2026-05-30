# Vendor Invoice Intelligence System  
**Freight Cost Prediction & Invoice Risk Flagging**  📌

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Business Objectives](#business-objectives)
- [Data Sources](#data-sources)
- [Exploratory Data Analysis](#eda)
- [Models Used](#models-used)
- [Evaluation Metrics](#metrics)
- [Application](#application)
- [Project Structure](#project-structure)
- [How to Run This Project](#how-to-run-this-project)
- [Author & Contact](#author--contact)

---

## 📌 <a id="project-overview"></a>Project Overview

This project is an **end-to-end machine learning system** I developed to automate and optimize financial workflows. It is designed to act as an intelligent layer for finance and procurement teams by:

1. **Predicting expected freight costs** for vendor invoices based on historical data.
2. **Flagging high-risk invoices** that require manual review due to anomalous cost, freight, or operational patterns.

Built entirely with Python, this project bridges the gap between raw database records and actionable business intelligence using predictive modeling and a clean, interactive web UI.

---

## 🎯 <a id="business-objectives"></a>Business Objectives

### 1. Freight Cost Prediction (Regression)

**Objective:** Predict the expected freight cost for a vendor invoice using factors like quantity, invoice value, and historical purchasing behavior.

**Why it matters:**
- Freight is a major, fluctuating component of landed cost.
- Accurate early predictions improve procurement planning, budgeting, and leverage during vendor negotiations.

*(Add a screenshot of your freight prediction UI here:
![](images/freight_prediction.png)')*

---

### 2. Invoice Risk Flagging (Classification)

**Objective:** Classify whether a vendor invoice should be flagged for manual approval due to abnormal patterns.

**Why it matters:**
- Manual invoice review is tedious and does not scale with high transaction volumes.
- Financial leakage and compliance risks often hide inside large, complex invoices.
- This automated flagging system lets finance teams focus strictly on high-risk anomalies while allowing standard invoices to process automatically.

*(Add a screenshot of your invoice flagging UI here: 
![](images/flag_invoice_prediction.png)`)*

---

## 📂 <a id="data-sources"></a>Data Sources

Data is structured in a relational SQLite database (`inventory.db`) containing the following core tables:

- `vendor_invoice` – Invoice-level financial and timing data  
- `purchases` – Item-level purchase details  
- `purchase_prices` – Reference purchase prices  
- `begin_inventory`, `end_inventory` – Inventory snapshots  

I utilized SQL aggregations and Python data manipulation to engineer comprehensive **invoice-level features** for the machine learning pipeline.

---

## 📊 <a id="eda"></a>Exploratory Data Analysis (EDA)

The EDA phase was heavily focused on answering **business-driven questions**:

- Do flagged invoices consistently present higher financial exposure?
- Is the relationship between freight cost and item quantity linear?
- How do historical price deviations impact current invoice risk?

I utilized statistical testing (such as t-tests via SciPy) to mathematically confirm that the features of "flagged" invoices differed meaningfully from standard, safe invoices.

---

## 🤖 <a id="models-used"></a>Models Used

### Regression (Freight Prediction)
- Linear Regression (Baseline)
- Decision Tree Regressor
- **Random Forest Regressor (Final Selected Model)**

### Classification (Invoice Flagging)
- Logistic Regression (Baseline)
- Decision Tree Classifier
- **Random Forest Classifier (Final Selected Model)**

*Note: Hyperparameter tuning was performed using **GridSearchCV**, optimizing for the F1-score to aggressively handle class imbalances in the risk-flagging dataset.*

---

## 📈 <a id="metrics"></a>Evaluation Metrics

### Freight Prediction
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

### Invoice Flagging
- Accuracy
- Precision, Recall, and F1-score
- Comprehensive Classification Reports
- Feature Importance Analysis (to provide explainability for *why* an invoice was flagged)

---

## 🖥 <a id="application"></a>End-to-End Application

I built a **Streamlit application** to serve as the user-facing portal for this intelligence system. The app allows users to:

- Input raw invoice details via a clean UI.
- Generate real-time freight cost predictions.
- Evaluate the risk status of an invoice instantly.
- View human-readable explanations of the model's decisions.

---

## 📁 <a id="project-structure"></a>Project Structure

```text
inventory-invoice-analytics/
│
├── data/
│   └── inventory.db
│
├── freight_cost_prediction/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── invoice_flagging/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── inference/
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
│
├── models/
│   ├── predict_freight_model.pkl
│   ├── scaler.pkl
│   └── predict_flag_invoice.pkl
│
├── notebooks/
│   ├── Invoice_Flagging.ipynb
│   └── Predict_Freight_Cost.ipynb
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
