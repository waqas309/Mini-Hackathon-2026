**Team Members:**
* **Waqas Ahmed** — CMS: `023-24-0031` | Builder (Data & Preprocessing)
* **Farman Ali** — CMS: `023-24-0032` | Builder (ML Modeling & Backend)
* **Marvi Malik** — CMS: `023-24-0016` | Product Lead & Front-End Builder

---

# Leukopenia / CBC Blood Analyzer

> Enter a Complete Blood Count (CBC) report and get an instant low-white-cell (leukopenia) risk screen, with every out-of-range blood parameter highlighted.

**Live demo:** <Streamlit Cloud link, add after deployment>  
**Demo video (60–90 s):** <video link, add after recording>

## Problem
Leukopenia (a low white blood cell count below $4.0 \times 10^3/\mu\text{L}$) leaves patients vulnerable to severe infections, yet early drops in routine Complete Blood Count (CBC) reports are often overlooked before a full clinical consultation. A fast, automated screening tool can flag high-risk blood panels immediately.

## Solution
A Streamlit web application powered by a trained **Random Forest Classifier** (with `StandardScaler` preprocessing) that evaluates 11 CBC parameters, estimates leukopenia probability, and highlights out-of-range lab values on a structured clinical slip.

## 3 MVP Features
1. **CBC Input Form & Presets:** Input panel for 9 hematological parameters (`WBC`, `RBC`, `HGB`, `PCV`, `PLT`, `MCV`, `MCH`, `MCHC`, `RDW`) plus `Age` and `Gender`, complete with one-click *Normal* and *Leukopenia* sample loaders.
2. **ML Risk Screening Engine:** Predicts leukopenia risk using a serialized Random Forest model (`models/best_model.pkl`) trained with `class_weight="balanced"` to address class imbalance (95.5% normal vs. 4.5% leukopenia cases).
3. **Clinical Insight & Lab Slip Panel:** Plots patient `WBC` against the normal $4.0 - 11.0 \times 10^3/\mu\text{L}$ clinical reference band and displays a color-coded lab slip flagging every low (`L`) or high (`H`) metric.

| Input Form | Screening Result | Lab Slip Breakdown |
| --- | --- | --- |
| *(Add form screenshot)* | *(Add result screenshot)* | *(Add lab slip screenshot)* |

## Model Benchmark & Evaluation (`notebooks/02_model_training.ipynb`)
We evaluated 5 classifiers on a stratified 80/20 split of 356 cleaned patient CBC records (`StandardScaler` fitted strictly on `X_train` to prevent data leakage):

| Model | Accuracy | Precision | Recall | F1-Score |
| --- | :---: | :---: | :---: | :---: |
| **Random Forest (Selected)** | **1.0000** | **1.0000** | **1.0000** | **1.00** |
| Decision Tree | 1.0000 | 1.0000 | 1.0000 | 1.00 |
| SVM (RBF) | 0.9722 | 0.6000 | 1.0000 | 0.75 |
| Logistic Regression | 0.9444 | 0.4286 | 1.0000 | 0.60 |
| KNN ($k=5$) | 0.9722 | 1.0000 | 0.3333 | 0.50 |

> **Note on Target Definition:** Because clinical leukopenia is defined by `WBC < 4.0`, tree-based models isolate that threshold cleanly (`1.0000` Recall). We also ran a secondary experiment dropping `WBC` (`0.9722` Accuracy, `0.3333` Recall) to verify multi-marker correlations across `RBC`, `HGB`, and `PLT`.

## Tech Stack & Project Structure
* **Tech Stack:** Python, pandas, NumPy, scikit-learn, joblib, Streamlit (deployed on Streamlit Community Cloud).
* **Repository Layout:**
  * `Data/` — `raw_cbc.csv` and `cleaned_cbc.csv` (356 records, 12 columns)
  * `notebooks/` — `01_preprocessing.ipynb` and `02_model_training.ipynb`
  * `models/` — `best_model.pkl`, `scaler.pkl`, and `feature_cols.pkl`
  * `src/predictor.py` — Prediction backend & clinical reference range checker
  * `app.py` — Streamlit web interface

## How to Run Locally
```bash
git clone [https://github.com/waqas309/Mini-Hackathon-2026.git](https://github.com/waqas309/Mini-Hackathon-2026.git)
cd Mini-Hackathon-2026
pip install -r requirements.txt
python -m streamlit run app.py