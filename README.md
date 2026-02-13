# 🚀 Customer Churn Prediction System

> Production-Grade Machine Learning Decision Engine for Telecom / SaaS Retention Strategy

---

## 📌 Project Overview

Customer churn directly impacts recurring revenue businesses such as Telecom and SaaS companies. This project builds a **production-style churn prediction system** that:

* Predicts customer churn probability
* Segments customers into risk tiers
* Recommends retention strategies
* Quantifies expected revenue at risk
* Exposes the system via a FastAPI inference API

This is not a notebook-only ML project — it is an **end-to-end deployable decision engine**.

---

## 🏗️ System Architecture

```
Client
   ↓
FastAPI Endpoint
   ↓
Sklearn Pipeline (Encoding + Scaling + Model)
   ↓
Decision Engine (Risk + Revenue Logic)
   ↓
Explanation Layer
   ↓
Structured JSON Response
```

### 📂 Project Structure

```
src/
 ├── data/                # Data loading & leakage audit
 ├── features/            # Feature engineering layer (reserved)
 ├── models/              # Training pipelines
 ├── api/                 # FastAPI app
 └── services/            # Decision engine & explanation logic
```

---

## 📊 Dataset

* **Dataset:** IBM Telco Customer Churn
* **Rows:** 7,043
* **Columns:** 33
* **Target:** `Churn Label`

### 🔒 Data Leakage Removal

The following columns were removed explicitly to prevent leakage:

* `Churn Score`
* `Churn Reason`
* `Churn Value`
* `CLTV`
* Identifiers (`CustomerID`, `Count`)
* Location metadata

Leakage detection was handled before modeling.

---

## 🤖 Modeling Strategy

### Models Evaluated

* Logistic Regression
* Decision Tree
* Random Forest

### ✅ Production Model: Logistic Regression

Chosen because:

* Competitive **ROC-AUC (~0.84)**
* Strong interpretability (coefficient analysis)
* Stable and less prone to overfitting
* Business-aligned threshold tuning

---

## 📈 Evaluation Metrics

* Accuracy
* Precision (Churn class)
* Recall (Churn class)
* ROC-AUC
* Confusion Matrix

### 🎯 Threshold Strategy

Default threshold (0.5) was replaced with **0.35** to prioritize recall and minimize false negatives in churn detection.

---

## 🧠 Decision Engine

The decision layer converts probability into business action.

### Risk Segmentation

| Probability | Risk Tier |
| ----------- | --------- |
| > 0.60      | High      |
| 0.35–0.60   | Medium    |
| < 0.35      | Low       |

### Retention Strategy Mapping

* 🔴 High Risk → Proactive call + Contract conversion
* 🟡 Medium Risk → Engagement email + Support bundle
* 🟢 Low Risk → Monitor only

### 💰 Expected Revenue at Risk

```
Expected Revenue = Churn Probability × Average CLTV
```

---

## 🌐 FastAPI Inference Endpoint

### Endpoint

```
POST /predict
```

### Sample Response

```json
{
  "churn_probability": 0.8064,
  "churn_prediction": "Yes",
  "risk_tier": "High",
  "recommended_action": "Proactive call + contract conversion incentive",
  "expected_revenue_at_risk": 8063.78,
  "explanation": "Customer is at high risk due to low tenure, month-to-month contract."
}
```

---

## 🛠️ Tech Stack

* Python
* Pandas / NumPy
* Scikit-learn
* FastAPI
* Uvicorn
* Joblib

---

## 🚀 How To Run

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Train Model

```
python src/models/train_baseline.py
```

### 3️⃣ Run API

```
uvicorn src.api.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🔮 Future Improvements

* SHAP-based explanation layer
* Individualized CLTV modeling
* Cross-validation stability testing
* Model calibration analysis
* Drift monitoring pipeline
* Cloud deployment with monitoring

---

## 🎓 Key Learnings

* Importance of leakage-safe modeling
* Threshold tuning over blind accuracy optimization
* Separation of model layer and business logic
* Designing ML systems as APIs
* Translating ML outputs into business actions

---

## 👤 Author

**Pratham Ingole**
Full Stack Data Science 
Project --> Customer Churn Decision Engine