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
    "신장(5cm단위)",
    "신장(5Cm단위)",
]

WEIGHT_COLUMN_CANDIDATES = [
    "weight",
    "weight_kg",
    "몸무게",
    "체중",
    "체중(5kg단위)",
    "체중(5Kg단위)",
]

TARGET_COLUMN_CANDIDATES = [
    "obesity",
    "is_obese",
    "target",
    "label",
    "비만여부",
    "비만",
]


def load_dataset(data_path):
    data_path = resolve_data_path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {data_path}")

    if data_path.suffix.lower() == ".csv":
        return read_csv_with_encoding_fallback(data_path)

    if data_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(data_path)

    raise ValueError("csv, xlsx, xls 파일만 지원합니다.")


def resolve_data_path(data_path):
    data_path = Path(data_path)
    if data_path.exists():
        return data_path

    parent = data_path.parent if str(data_path.parent) else Path(".")
    if not parent.exists():
        return data_path

    target_name = data_path.name.lower()
    for candidate in parent.iterdir():
        if candidate.name.lower() == target_name:
            return candidate

    return data_path


def read_csv_with_encoding_fallback(data_path):
    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]
    last_error = None

    for encoding in encodings:
        try:
            return pd.read_csv(data_path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError as error:
            last_error = error

    raise last_error


def find_column(dataframe, candidates):
    normalized_columns = {
        normalize_column_name(column): column
        for column in dataframe.columns
    }

    for candidate in candidates:
        key = normalize_column_name(candidate)
        if key in normalized_columns:
            return normalized_columns[key]

    return None


def normalize_column_name(column):
    return str(column).strip().lower().replace(" ", "")


def preprocess_dataset(raw_dataframe):
    height_column = find_column(raw_dataframe, HEIGHT_COLUMN_CANDIDATES)
    weight_column = find_column(raw_dataframe, WEIGHT_COLUMN_CANDIDATES)
    target_column = find_column(raw_dataframe, TARGET_COLUMN_CANDIDATES)

    if height_column is None or weight_column is None:
        raise ValueError(
            "키와 몸무게 컬럼을 찾지 못했습니다. "
            f"현재 컬럼: {list(raw_dataframe.columns)}"
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

    if dataframe.empty:
        raise ValueError("전처리 후 학습 가능한 데이터가 없습니다.")

    if dataframe["is_obese"].nunique() < 2:
        raise ValueError("정상/비만 데이터가 모두 있어야 모델을 학습할 수 있습니다.")

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

    model = Pipeline(
        steps=[
            (
                "preprocessor",
                ColumnTransformer(
                    transformers=[
                        ("numeric", StandardScaler(), ["height", "weight"]),
                    ]
                ),
            ),
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
        "model_type": "sklearn_logistic_regression",
        "features": ["height", "weight"],
        "target": "is_obese",
        "obesity_rule": "target column이 없으면 BMI >= 25 기준으로 is_obese 생성",
        "sample_count": int(len(training_dataframe)),
        "normal_count": int((training_dataframe["is_obese"] == 0).sum()),
        "obese_count": int(training_dataframe["is_obese"].sum()),
        "average_height": round(float(training_dataframe["height"].mean()), 2),
        "average_weight": round(float(training_dataframe["weight"].mean()), 2),
        "average_bmi": round(float(training_dataframe["bmi"].mean()), 2),
        "min_bmi": round(float(training_dataframe["bmi"].min()), 2),
        "max_bmi": round(float(training_dataframe["bmi"].max()), 2),
        "metrics": metrics,
    }

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(description="건강검진 데이터 기반 비만 예측 모델 학습")
    parser.add_argument(
        "--data",
        default="data/health_checkup.csv",
        help="학습 데이터 경로",
    )
    parser.add_argument(
        "--model-output",
        default="models/obesity_model.pkl",
        help="학습된 모델 저장 경로",
    )
    parser.add_argument(
        "--metadata-output",
        default="models/obesity_model_metadata.json",
        help="모델 메타데이터 저장 경로",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"데이터 로드: {args.data}")
    raw_dataframe = load_dataset(args.data)

    print("데이터 전처리 시작")
    training_dataframe = preprocess_dataset(raw_dataframe)

    print("모델 학습 시작")
    model, metrics = train_model(training_dataframe)

    save_model(model, args.model_output)
    save_metadata(training_dataframe, metrics, args.metadata_output)

    print(f"모델 저장 완료: {args.model_output}")
    print(f"메타데이터 저장 완료: {args.metadata_output}")
    print(f"학습 데이터 수: {len(training_dataframe)}")
    print(f"정상 데이터 수: {(training_dataframe['is_obese'] == 0).sum()}")
    print(f"비만 데이터 수: {training_dataframe['is_obese'].sum()}")
    print(f"정확도: {metrics['accuracy']:.4f}")


if __name__ == "__main__":
    main()
