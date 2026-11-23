import os
import joblib
import pandas as pd

# Resolve paths dynamically so it works from both root (app.py) and subfolders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
FEATURE_COLS = joblib.load(COLS_PATH)

def predict_leukopenia(patient_data: dict) -> dict:
    """
    Takes a dictionary of 11 CBC parameters and returns the Random Forest prediction,
    probability percentage, and clinically flagged out-of-range parameters.
    """
    # Convert Gender string to numeric (0.0 = Female, 1.0 = Male) if passed as text
    data = patient_data.copy()
    if isinstance(data.get("Gender"), str):
        data["Gender"] = 1.0 if data["Gender"].strip().lower() == "male" else 0.0

    # Arrange columns in the exact order used during training
    input_df = pd.DataFrame([data])[FEATURE_COLS]
    input_scaled = scaler.transform(input_df)

    pred = int(model.predict(input_scaled)[0])
    prob = float(model.predict_proba(input_scaled)[0][1]) * 100

    # Clinical range checks for UI lab slip breakdown
    flags = []
    if data["WBC"] < 4.0:
        flags.append(f"White cells (WBC) is low ({data['WBC']} x10^3/uL; normal 4.0 - 11.0)")
    elif data["WBC"] > 11.0:
        flags.append(f"White cells (WBC) is elevated ({data['WBC']} x10^3/uL; normal 4.0 - 11.0)")

    if data["RBC"] < 4.2:
        flags.append(f"Red cells (RBC) is low ({data['RBC']} x10^6/uL; normal 4.2 - 5.9)")
    if data["HGB"] < 12.0:
        flags.append(f"Hemoglobin (HGB) is low ({data['HGB']} g/dL; normal 12.0 - 17.5)")
    if data["PLT"] < 150.0:
        flags.append(f"Platelets (PLT) is low ({data['PLT']} x10^3/uL; normal 150 - 450)")

    return {
        "prediction": pred,
        "label": "Leukopenia risk detected" if pred == 1 else "No leukopenia signal",
        "risk_probability": round(prob, 1),
        "flagged_metrics": flags
    }

# Quick self-test when running `python src/predictor.py` directly
if __name__ == "__main__":
    sample_normal = {
        "Age": 34, "Gender": "Male", "RBC": 4.90, "PCV": 42.0, "MCV": 89.0,
        "MCH": 29.5, "MCHC": 33.5, "RDW": 13.0, "WBC": 6.80, "PLT": 260.0, "HGB": 14.2
    }
    sample_risk = {
        "Age": 45, "Gender": "Female", "RBC": 3.40, "PCV": 31.0, "MCV": 82.0,
        "MCH": 27.0, "MCHC": 32.0, "RDW": 15.8, "WBC": 2.60, "PLT": 115.0, "HGB": 10.1
    }
    print("Normal Test:", predict_leukopenia(sample_normal))
    print("Risk Test:", predict_leukopenia(sample_risk))