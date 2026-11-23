import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
FEATURE_COLS = joblib.load(COLS_PATH)

REF_RANGES = [
    ("WBC", 4.0, 11.0),
    ("RBC", 4.2, 5.9),
    ("HGB", 12.0, 17.5),
    ("PCV", 36.0, 52.0),
    ("PLT", 150.0, 450.0),
    ("MCV", 80.0, 100.0),
    ("MCH", 27.0, 33.0),
    ("MCHC", 32.0, 36.0),
    ("RDW", 11.5, 14.5),
]

def predict_leukopenia(values: dict) -> dict:
    """
    Matches app.py's exact expected contract:
    returns {"prediction": int, "probability": float (0-1), "flagged_metrics": list[str]}
    """
    data = values.copy()
    if isinstance(data.get("Gender"), str):
        data["Gender"] = 1 if data["Gender"].strip().lower() == "male" else 0

    input_df = pd.DataFrame([data])[FEATURE_COLS]
    input_scaled = scaler.transform(input_df)

    pred = int(model.predict(input_scaled)[0])
    prob = float(model.predict_proba(input_scaled)[0][1])  # 0.0 to 1.0 float for app.py

    flags = []
    for key, lo, hi in REF_RANGES:
        v = data[key]
        if v < lo:
            flags.append(f"{key} low ({v:g} < {lo:g})")
        elif v > hi:
            flags.append(f"{key} high ({v:g} > {hi:g})")

    return {
        "prediction": pred,
        "probability": prob,
        "flagged_metrics": flags,
    }