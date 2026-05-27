# Spring-Flask 예측 연동 구현 계획

## 목표

Spring Boot에서 사용자의 키와 몸무게 입력을 받아 Flask AI 서버의 `/predict` API로 전달하고,
반환된 비만 여부 예측 결과를 Thymeleaf 화면에 출력한다.

## 구현 순서

### 1단계 - DTO 생성

### 생성 파일

- `spring-server/src/main/java/com/example/loginproject/dto/PredictRequestDto.java`
- `spring-server/src/main/java/com/example/loginproject/dto/PredictResponseDto.java`

### 역할

- `PredictRequestDto`: 화면 입력값과 Flask 요청 JSON 데이터 관리
- `PredictResponseDto`: Flask 응답 JSON 데이터 관리

---

### 2단계 - RestTemplate 설정 및 Service 생성

### 생성 파일

- `spring-server/src/main/java/com/example/loginproject/config/RestTemplateConfig.java`
- `spring-server/src/main/java/com/example/loginproject/service/PredictService.java`

### 수정 파일

- `spring-server/src/main/resources/application.yml`

### 역할

- `RestTemplate` Bean 등록
- Flask 서버 URL 설정값 관리
- Flask `/predict` API로 POST 요청 전송
- JSON 응답을 DTO로 변환

---

### 3단계 - Controller 생성

### 생성 파일

- `spring-server/src/main/java/com/example/loginproject/controller/PredictController.java`

### 역할

- `GET /predict`: 예측 입력 폼 표시
- `POST /predict`: 입력값 검증 후 Flask 예측 요청
- 예측 결과를 결과 화면에 전달

---

### 4단계 - Thymeleaf 화면 생성

### 생성 파일

- `spring-server/src/main/resources/templates/predict/form.html`
- `spring-server/src/main/resources/templates/predict/result.html`

### 역할

- 키와 몸무게 입력 화면 구성
- 예측 결과 출력 화면 구성

---

### 5단계 - SecurityConfig 확인

### 수정 파일

- `spring-server/src/main/java/com/example/loginproject/config/SecurityConfig.java`

### 역할

- `/predict`, `/predict/**` 비회원 접근 허용

## Flask API 형식

### Request

```json
{
  "height": 170,
  "weight": 70
}
```

### Response

```json
{
  "result": "정상"
}
```
