from pathlib import Path
import json, sys
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Employee.csv"
OUT = ROOT / "backend" / "model"
FEATURES = ["Education", "JoiningYear", "City", "PaymentTier", "Age", "Gender", "EverBenched", "ExperienceInCurrentDomain"]
TARGET = "LeaveOrNot"
NUM = ["JoiningYear", "PaymentTier", "Age", "ExperienceInCurrentDomain"]
CAT = ["Education", "City", "Gender", "EverBenched"]

def main():
    if not DATA.exists():
        sys.exit(f"Dataset not found: {DATA}. Put Employee.csv in data/.")
    df = pd.read_csv(DATA)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        sys.exit(f"Missing required columns: {missing}")
    df = df[FEATURES + [TARGET]].drop_duplicates().copy()
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df[df[TARGET].isin([0, 1])]
    if df[TARGET].nunique() != 2:
        sys.exit("LeaveOrNot must contain both 0 (stay) and 1 (leave).")
    X, y = df[FEATURES], df[TARGET].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    pre = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUM),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CAT)
    ])
    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced", min_samples_leaf=2)
    }
    pipes, scores = {}, {}
    for name, clf in models.items():
        pipe = Pipeline([("preprocess", pre), ("classifier", clf)])
        pipe.fit(X_train, y_train)
        pred, proba = pipe.predict(X_test), pipe.predict_proba(X_test)[:, 1]
        scores[name] = {
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist()
        }
        pipes[name] = pipe
        print("\n" + name, json.dumps(scores[name], indent=2))
        print(classification_report(y_test, pred, zero_division=0))
    best = max(scores, key=lambda n: scores[n]["f1"])
    OUT.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipes[best], OUT / "pipeline.pkl")
    report = {"best_model": best, "target": TARGET, "features": FEATURES, "test_rows": int(len(y_test)), "models": scores}
    try:
        pipe = pipes[best]
        names = pipe.named_steps["preprocess"].get_feature_names_out()
        clf = pipe.named_steps["classifier"]
        vals = getattr(clf, "feature_importances_", None)
        if vals is None and hasattr(clf, "coef_"):
            vals = abs(clf.coef_[0])
        if vals is not None:
            report["feature_importance"] = dict(sorted(((str(n), round(float(v), 6)) for n, v in zip(names, vals)), key=lambda x: x[1], reverse=True)[:20])
    except Exception:
        report["feature_importance"] = {}
    (OUT / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nSelected {best}. Saved model and metrics under {OUT}")

if __name__ == "__main__":
    main()
