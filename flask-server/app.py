from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "obesity_model.pkl"


def create_app():
    app = Flask(__name__)
    CORS(app)

    model = load_model()

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "잘못된 요청입니다."}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "요청한 API를 찾을 수 없습니다."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"message": "서버 내부 오류가 발생했습니다."}), 500

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/predict")
    def predict():
        try:
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"message": "JSON 요청 본문이 필요합니다."}), 400

            height = parse_number(data.get("height"), "height")
            weight = parse_number(data.get("weight"), "weight")
            validate_input(height, weight)

            bmi = calculate_bmi(height, weight)
            result = predict_result(model, height, weight, bmi)

            return jsonify({"result": result})
        except ValueError as error:
            return jsonify({"message": str(error)}), 400
        except Exception:
            return jsonify({"message": "예측 처리 중 오류가 발생했습니다."}), 500

    return app


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {MODEL_PATH}")

    return joblib.load(MODEL_PATH)


def parse_number(value, field_name):
    if value is None:
        raise ValueError(f"{field_name} 값을 입력해주세요.")

    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} 값은 숫자여야 합니다.")


def validate_input(height, weight):
    if height < 100 or height > 250:
        raise ValueError("height는 100cm 이상 250cm 이하로 입력해주세요.")

    if weight < 25 or weight > 250:
        raise ValueError("weight는 25kg 이상 250kg 이하로 입력해주세요.")


def calculate_bmi(height, weight):
    return weight / ((height / 100) ** 2)


def predict_result(model, height, weight, bmi):
    if isinstance(model, dict) and model.get("model_type") == "bmi_rule":
        threshold = float(model.get("obesity_bmi_threshold", 25.0))
        label = model.get("obese_label", "obese") if bmi >= threshold else model.get("normal_label", "normal")
        return to_korean_label(label)

    input_data = pd.DataFrame([{"height": height, "weight": weight}])
    prediction = model.predict(input_data)[0]
    return to_korean_label(prediction)


def to_korean_label(label):
    if str(label).strip().lower() in ["1", "true", "obese", "비만"]:
        return "비만"

    return "정상"


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
