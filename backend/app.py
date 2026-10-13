from pathlib import Path
import json
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "backend" / "model" / "pipeline.pkl"
METRICS_PATH = ROOT / "backend" / "model" / "metrics.json"
FEATURES = ["Education", "JoiningYear", "City", "PaymentTier", "Age", "Gender", "EverBenched", "ExperienceInCurrentDomain"]
NUM = ["JoiningYear", "PaymentTier", "Age", "ExperienceInCurrentDomain"]
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://employee-attrition-prediction-syste-sigma.vercel.app",
        ]
    }
})
_model = None

def get_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model

@app.get("/")
def home():
    return jsonify({"name": "Employee Attrition Prediction API", "status": "running", "endpoints": ["/health", "/model-info", "/predict"]})

@app.get("/health")
def health():
    exists = MODEL_PATH.exists()
    return jsonify({"status": "ok" if exists else "model_not_trained", "model_file_exists": exists}), (200 if exists else 503)

@app.get("/model-info")
def model_info():
    if not METRICS_PATH.exists():
        return jsonify({"error": "Train the model first."}), 404
    return jsonify(json.loads(METRICS_PATH.read_text(encoding="utf-8")))

@app.post("/predict")
def predict():
    model = get_model()
    if model is None:
        return jsonify({"error": "Model missing. From the project root run: python backend/train_model.py"}), 503
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"error": "Send a JSON object."}), 400
    missing = [f for f in FEATURES if f not in body]
    if missing:
        return jsonify({"error": "Missing fields: " + ", ".join(missing)}), 400
    try:
        row = {f: body[f] for f in FEATURES}
        for f in NUM:
            row[f] = float(row[f])
        frame = pd.DataFrame([row], columns=FEATURES)
        prediction = int(model.predict(frame)[0])
        probability = float(model.predict_proba(frame)[0][1]) if hasattr(model, "predict_proba") else None
        return jsonify({"prediction": prediction, "label": "Leave" if prediction == 1 else "Stay", "probability_leave": probability, "message": "Statistical estimate only, not a certainty."})
    except (TypeError, ValueError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({"error": "Prediction failed. Check backend logs."}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
