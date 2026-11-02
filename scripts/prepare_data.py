"""Recreate the dissertation's deterministic cleaning rules from the source CSV."""
from pathlib import Path
import argparse
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def clean(raw):
    frame = raw.drop(columns=["id"]).copy()
    frame["age_years"] = frame["age"] / 365.25
    frame = frame.drop(columns=["age"])
    frame = frame[
        frame["height"].between(100, 230)
        & frame["weight"].between(30, 250)
        & frame["ap_hi"].between(70, 300)
        & frame["ap_lo"].between(40, 200)
        & (frame["ap_hi"] > frame["ap_lo"])
    ].copy()
    frame["BMI"] = frame["weight"] / ((frame["height"] / 100) ** 2)
    frame["pulse_pressure"] = frame["ap_hi"] - frame["ap_lo"]
    frame = frame[frame["BMI"].between(10, 70)].copy()
    columns = ["age_years", "gender", "height", "weight", "BMI", "ap_hi",
               "ap_lo", "pulse_pressure", "cholesterol", "gluc", "smoke",
               "alco", "active", "cardio"]
    return frame[columns].reset_index(drop=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    raw = pd.read_csv(args.input, sep=";")
    cleaned = clean(raw)
    if len(raw) != 70000 or len(cleaned) != 68627:
        raise ValueError("This file does not reproduce the dissertation's 70,000 → 68,627 rows.")
    destination = ROOT / "data"
    destination.mkdir(exist_ok=True)
    raw.to_csv(destination / "cardio_train.csv", sep=";", index=False)
    cleaned.to_csv(destination / "cardio_final.csv", index=False)
    print(f"Prepared {len(cleaned):,} rows; removed {len(raw)-len(cleaned):,}.")
