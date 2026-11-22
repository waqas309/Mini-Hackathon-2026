/* Enter Your Name and CMS ID */

Name: Waqas Ahmed CMS: 023-24-0031

Name: Farman Ali CMS: 023-24-0032

Name: Marvi Malik CMS: 023-24-0016



---

# Leukopenia / CBC Blood Analyzer

> Paste a Complete Blood Count and get an instant low-white-cell (leukopenia) risk screen, with the out-of-range values highlighted.

**Live demo:** <Streamlit Cloud link, add after deployment>  
**Demo video (60-90 s):** <video link, add after recording>

## Problem
Leukopenia (a low white blood cell count) can leave the body open to infections, but it is often only noticed after a routine CBC is read carefully by a clinician. A quick, readable first screen from CBC values can help flag cases early.

## Solution
A Streamlit web app where the user enters CBC values and a trained machine learning model estimates the risk of leukopenia, showing the probability and which values fall outside their normal range.

## 3 MVP Features
1. **CBC input form** with 9 blood parameters plus age and gender, and quick-fill Normal / Leukopenia sample buttons.
2. **Risk prediction** from a trained classifier with a saved StandardScaler, shown as a risk label with a probability.
3. **Clinical insight panel**: WBC plotted against the normal 4.0 to 11.0 range, plus a lab-slip table that flags every out-of-range value.

| Screenshot 1 | Screenshot 2 | Screenshot 3 |
| --- | --- | --- |
| (form screenshot) | (result screenshot) | (lab slip screenshot) |

## Tech Stack
Python, pandas, NumPy, scikit-learn, joblib, Streamlit (Streamlit Community Cloud).

## How to Run Locally
```bash
git clone https://github.com/waqas309/Mini-Hackathon-2026.git
cd Mini-Hackathon-2026
pip install -r requirements.txt
streamlit run app.py
```

## Team & Roles
| Member | Role |
| --- | --- |
| Waqas Ahmed | Data sourcing, cleaning and preprocessing |
| Farman Ali | Model training, evaluation and prediction module |
| Marvi Malik | Streamlit UI, README, deployment, demo video and pitch |

## AI Log
Mistakes made by the AI assistant that the team caught and fixed.

| # | What the AI suggested or got wrong | How we noticed | How we fixed it |
| --- | --- | --- | --- |
| 1 | The AI-generated first version of `app.py` used the feature name `HCT` and had no `RDW` input, based on a generic CBC layout rather than our dataset. | We printed the header of `cleaned_cbc.csv` (Age, Gender, RBC, PCV, MCV, MCH, MCHC, RDW, WBC, PLT, HGB) and compared it with the feature list in the app. | Renamed `HCT` to `PCV`, added an `RDW` input with its normal range (11.5 to 14.5 %), updated both sample presets, and re-tested the normal and leukopenia samples.

## Future Improvements
- Extend the screen to other blood disorders (anemia, thrombocytopenia).
- Train on larger, multi-source data and check how well the probabilities are calibrated.
- Read values automatically from an uploaded lab report.

