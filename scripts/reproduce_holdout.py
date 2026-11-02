"""Rerun the seven primary estimators; keep new outputs apart from reported results.

This does not rerun hyperparameter searches, five-fold CV, ablations or threshold
experiments. For the complete workflow, use notebooks/analysis.ipynb.
"""
from pathlib import Path
import json
import platform
import importlib.metadata
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from _model_definitions import models

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/cardio_final.csv")
features = ["age_years", "gender", "BMI", "ap_hi", "ap_lo", "cholesterol",
            "gluc", "smoke", "alco", "active"]
X_train, X_test, y_train, y_test = train_test_split(
    df[features], df["cardio"], test_size=0.2, random_state=42, stratify=df["cardio"]
)
rows = []
for name, estimator in models.items():
    estimator.fit(X_train, y_train)
    pred = estimator.predict(X_test)
    score = (estimator.predict_proba(X_test)[:, 1] if hasattr(estimator, "predict_proba")
             else estimator.decision_function(X_test))
    rows.append({"Model": name, "Accuracy": accuracy_score(y_test, pred),
                 "Precision": precision_score(y_test, pred, zero_division=0),
                 "Recall": recall_score(y_test, pred, zero_division=0),
                 "F1": f1_score(y_test, pred, zero_division=0),
                 "ROC-AUC": roc_auc_score(y_test, score)})
    print(name, {k: round(v, 4) for k, v in rows[-1].items() if k != "Model"}, flush=True)
out = ROOT / "results"
out.mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(out / "reproduced_model_comparison.csv", index=False)
(out / "reproduction_environment.json").write_text(json.dumps({
    "python": platform.python_version(),
    "packages": {p: importlib.metadata.version(p) for p in ["numpy", "pandas", "scikit-learn", "scipy"]},
    "train_rows": len(y_train), "test_rows": len(y_test),
    "scope": "Primary held-out model fit/evaluation only; no CV or tuning rerun."
}, indent=2) + "\n")
