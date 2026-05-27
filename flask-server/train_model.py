import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


HEIGHT_COLUMN_CANDIDATES = [
    "height",
    "height_cm",
    "키",
    "신장",
    "신장(5Cm단위)",
    "신장(5cm단위)",
]

WEIGHT_COLUMN_CANDIDATES = [
    "weight",
    "weight_kg",
    "몸무게",
    "체중",
    "체중(5Kg단위)",
    "체중(5kg단위)",
]

TARGET_COLUMN_CANDIDATES = [
    "obesity",
    "is_obese",
    "target",
    "label",
    "비만여부",
    "비만",
]


def find_column(dataframe, candidates):
    normalized_columns = {
        str(column).strip().lower(): column
        for column in dataframe.columns
    }

    for candidate in candidates:
        key = candidate.strip().lower()
        if key in normalized_columns:
            return normalized_columns[key]

    return None


def load_dataset(data_path):
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    if data_path.suffix.lower() == ".csv":
        return pd.read_csv(data_path)

    if data_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(data_path)

    raise ValueError("Only csv, xlsx, and xls files are supported.")


def build_training_dataframe(raw_dataframe):
    height_column = find_column(raw_dataframe, HEIGHT_COLUMN_CANDIDATES)
    weight_column = find_column(raw_dataframe, WEIGHT_COLUMN_CANDIDATES)
    target_column = find_column(raw_dataframe, TARGET_COLUMN_CANDIDATES)

    if height_column is None or weight_column is None:
        raise ValueError(
            "Height and weight columns are required. "
            f"Available columns: {list(raw_dataframe.columns)}"
        )

    dataframe = raw_dataframe[[height_column, weight_column]].copy()
    dataframe.columns = ["height", "weight"]

    dataframe["height"] = pd.to_numeric(dataframe["height"], errors="coerce")
    dataframe["weight"] = pd.to_numeric(dataframe["weight"], errors="coerce")
    dataframe = dataframe.dropna(subset=["height", "weight"])

    dataframe = dataframe[
        (dataframe["height"] >= 100)
        & (dataframe["height"] <= 250)
        & (dataframe["weight"] >= 25)
        & (dataframe["weight"] <= 250)
    ].copy()

    dataframe["bmi"] = dataframe["weight"] / ((dataframe["height"] / 100) ** 2)

    if target_column is not None:
        target_series = raw_dataframe.loc[dataframe.index, target_column]
        dataframe["is_obese"] = normalize_target(target_series)
    else:
        dataframe["is_obese"] = (dataframe["bmi"] >= 25).astype(int)

    dataframe = dataframe.dropna(subset=["is_obese"])
    dataframe["is_obese"] = dataframe["is_obese"].astype(int)

    if dataframe["is_obese"].nunique() < 2:
        raise ValueError("Training target must contain both obese and non-obese samples.")

    return dataframe


def normalize_target(target_series):
    positive_values = {"1", "true", "yes", "y", "obese", "비만"}
    negative_values = {"0", "false", "no", "n", "normal", "정상", "비비만"}

    def convert(value):
        if pd.isna(value):
            return None

        if isinstance(value, (int, float)):
            return 1 if value >= 1 else 0

        text = str(value).strip().lower()
        if text in positive_values:
            return 1
        if text in negative_values:
            return 0

        return None

    return target_series.map(convert)


def train_model(training_dataframe):
    features = training_dataframe[["height", "weight"]]
    target = training_dataframe["is_obese"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), ["height", "weight"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "classification_report": classification_report(
            y_test,
            predictions,
            target_names=["normal", "obese"],
            output_dict=True,
        ),
    }

    return model, metrics


def save_model(model, model_path):
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def save_metadata(training_dataframe, metrics, metadata_path):
    metadata_path = Path(metadata_path)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    metadata = {
        "features": ["height", "weight"],
        "target": "is_obese",
        "obesity_rule": "BMI >= 25 when target column is missing",
        "sample_count": int(len(training_dataframe)),
        "obese_count": int(training_dataframe["is_obese"].sum()),
        "normal_count": int((training_dataframe["is_obese"] == 0).sum()),
        "metrics": metrics,
    }

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(description="Train obesity prediction model.")
    parser.add_argument(
        "--data",
        default="data/health_checkup.csv",
        help="Path to health checkup dataset. csv, xlsx, and xls are supported.",
    )
    parser.add_argument(
        "--model-output",
        default="models/obesity_model.pkl",
        help="Path to save trained model.",
    )
    parser.add_argument(
        "--metadata-output",
        default="models/obesity_model_metadata.json",
        help="Path to save model metadata.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    raw_dataframe = load_dataset(args.data)
    training_dataframe = build_training_dataframe(raw_dataframe)
    model, metrics = train_model(training_dataframe)

    save_model(model, args.model_output)
    save_metadata(training_dataframe, metrics, args.metadata_output)

    print(f"Model saved to {args.model_output}")
    print(f"Metadata saved to {args.metadata_output}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")


if __name__ == "__main__":
    main()
