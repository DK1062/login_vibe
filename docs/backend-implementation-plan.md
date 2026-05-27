# 백엔드 기본 기능 구현 계획

## 0단계 - Spring Boot 기본 프로젝트 구조

### 생성 파일

- `spring-server/settings.gradle`
- `spring-server/build.gradle`
- `spring-server/src/main/java/com/example/loginproject/LoginProjectApplication.java`
- `spring-server/src/main/resources/application.yml`

### 목적

- Spring Boot, Spring Security, JPA, Thymeleaf, MySQL 의존성을 설정한다.
- 이후 회원, 게시판, 답글 기능을 추가할 기본 패키지 구조를 만든다.

---

## 1단계 - 회원가입 기본 기능

### 생성 파일

- `spring-server/src/main/java/com/example/loginproject/domain/Member.java`
- `spring-server/src/main/java/com/example/loginproject/domain/Role.java`
- `spring-server/src/main/java/com/example/loginproject/repository/MemberRepository.java`
- `spring-server/src/main/java/com/example/loginproject/dto/MemberSignupRequest.java`
- `spring-server/src/main/java/com/example/loginproject/dto/MemberResponse.java`
- `spring-server/src/main/java/com/example/loginproject/service/MemberService.java`
- `spring-server/src/main/java/com/example/loginproject/controller/MemberController.java`
- `spring-server/src/main/java/com/example/loginproject/config/PasswordEncoderConfig.java`
- `spring-server/src/main/resources/templates/member/signup.html`
- `spring-server/src/main/resources/templates/member/list.html`

### 구현 내용

- 아이디, 비밀번호, 이름을 입력받아 회원가입 처리
- 아이디 중복 검사
- BCrypt 기반 비밀번호 암호화
- 회원 목록 조회용 응답 DTO 구성
- 회원가입 화면 URL과 처리 URL 구성
- 회원가입 화면과 관리자 회원 목록 기본 화면 구성

### URL

- `GET /members/signup` 회원가입 화면
- `POST /members/signup` 회원가입 처리
- `GET /members` 회원 목록

---

## 2단계 - Spring Security 로그인/로그아웃

### 생성/수정 파일

- `spring-server/src/main/java/com/example/loginproject/config/SecurityConfig.java`
- `spring-server/src/main/java/com/example/loginproject/service/CustomUserDetailsService.java`
- `spring-server/src/main/java/com/example/loginproject/controller/LoginController.java`
- `spring-server/src/main/resources/templates/member/login.html`
- `spring-server/src/main/resources/templates/index.html`

### 구현 내용

- Spring Security formLogin 적용
- BCryptPasswordEncoder Bean 등록
- 로그인 성공 시 `/`로 이동
- 로그아웃 처리
- 비회원 접근 가능 URL 설정
- 관리자 전용 URL 설정

### URL

- `GET /login`
- `POST /login`
- `POST /logout`

---

## 3단계 - 게시판 CRUD

### 생성 파일

- `domain/Question.java`
- `repository/QuestionRepository.java`
- `dto/QuestionCreateRequest.java`
- `dto/QuestionUpdateRequest.java`
- `dto/QuestionResponse.java`
- `service/QuestionService.java`
- `controller/QuestionController.java`
- `templates/question/list.html`
- `templates/question/detail.html`
- `templates/question/form.html`
- `templates/question/edit.html`

### 구현 내용

- 게시글 목록, 상세, 등록, 수정, 삭제
- 작성자 정보 저장
- 로그인한 사용자만 접근 및 작성 가능
- 작성자 본인만 수정/삭제 가능
- 작성자가 없는 기존 게시글은 관리자만 수정/삭제 가능

### URL

- `GET /questions`
- `GET /questions/{id}`
- `GET /questions/new`
- `POST /questions`
- `GET /questions/{id}/edit`
- `POST /questions/{id}/edit`
- `POST /questions/{id}/delete`

---

## 4단계 - 답글 기능

### 생성 파일

- `domain/Answer.java`
- `repository/AnswerRepository.java`
- `dto/AnswerCreateRequest.java`
- `dto/AnswerUpdateRequest.java`
- `service/AnswerService.java`
- `controller/AnswerController.java`

### 구현 내용

- 게시글 상세 화면에서 답글 등록
- 답글 작성자 정보 저장
- 본인이 작성한 답글만 수정/삭제 가능

### URL

- `POST /boards/{boardId}/answers`
- `POST /answers/{answerId}/edit`
- `POST /answers/{answerId}/delete`

---

## 5단계 - 화면 및 검증 정리

### 생성/수정 파일

- `templates/layout/header.html`
- `templates/layout/footer.html`
- `templates/member/signup.html`
- `templates/member/list.html`
- `static/css/style.css`

### 구현 내용

- Bootstrap 기반 화면 구성
- 입력값 검증 메시지 출력
- 인증 상태에 따른 메뉴 표시
