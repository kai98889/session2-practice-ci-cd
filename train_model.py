"""Train a salary model and export its parameters and fitted estimator."""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def train(data_path: Path, output_dir: Path) -> LinearRegression:
    data = pd.read_csv(data_path)
    required = ["YearsExperience", "Salary"]
    if not set(required).issubset(data.columns):
        raise ValueError("CSV must contain YearsExperience and Salary columns")
    values = data[required].apply(pd.to_numeric, errors="raise")
    if len(values) < 2 or not np.isfinite(values.to_numpy()).all():
        raise ValueError("Provide at least two rows with finite numeric values")
    if values["YearsExperience"].nunique() < 2:
        raise ValueError("YearsExperience must contain at least two distinct values")

    model = LinearRegression().fit(values[["YearsExperience"]], values["Salary"])
    output_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_dir / "linear_model.pkl")
    (output_dir / "linear_model.txt").write_text(
        f"Coefficients: {model.coef_}\nIntercept: {model.intercept_}\n",
        encoding="utf-8",
    )
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("training_data.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    train(args.data, args.output_dir)
