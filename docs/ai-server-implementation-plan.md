# AI 서버 구현 계획

## 추천 폴더 구조

```text
flask-server/
 ┣ app.py
 ┣ train_model.py
 ┣ requirements.txt
 ┣ data/
 ┃ ┗ health_checkup.csv
 ┣ models/
 ┃ ┗ obesity_model.pkl
 ┗ README.md
```

## 1단계 - 데이터 전처리 및 모델 학습

### 생성 파일

- `flask-server/train_model.py`
- `flask-server/requirements.txt`
- `flask-server/data/.gitkeep`
- `flask-server/models/.gitkeep`

### 역할

- 건강검진 CSV 데이터 로드
- 키와 몸무게 컬럼 정리
- 결측치 및 이상치 제거
- 비만 여부 타깃 데이터 준비
- 학습 데이터와 테스트 데이터 분리
- Scikit-learn 모델 학습
- Joblib 파일로 모델 저장

### 실행 예시

```bash
python train_model.py --data data/health_checkup.csv
```

### 저장 결과

```text
models/obesity_model.pkl
```

---

## 2단계 - Flask 서버 기본 구성

### 생성 파일

- `flask-server/app.py`

### 역할

- Flask 앱 생성
- `flask-cors` 적용
- 저장된 모델 로드
- 서버 상태 확인 API 제공

### API

- `GET /health`

---

## 3단계 - 예측 API 구현

### 수정 파일

- `flask-server/app.py`

### 역할

- JSON 요청 파싱
- 키와 몸무게 입력값 검증
- 모델 예측 실행
- Spring Boot에서 처리하기 쉬운 JSON 응답 반환

### API

- `POST /predict`

### 요청 예시

```json
{
  "height": 175,
  "weight": 82
}
```

### 응답 예시

```json
{
  "prediction": "OBESE",
  "predictionLabel": "비만",
  "bmi": 26.78
}
```

---

## 4단계 - Spring Boot 연동 정리

### 역할

- Spring Boot에서 Flask `/predict` API 호출
- 요청/응답 DTO 구성
- 예측 결과 화면 출력
- 필요 시 예측 결과 DB 저장
