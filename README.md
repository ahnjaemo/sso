# Python FastAPI 인증 서비스

이 프로젝트는 Python FastAPI를 사용하여 구현된 현대적인 사용자 인증 API 서비스입니다. 표준 이메일/비밀번호 기반 인증과 Google 소셜 로그인을 모두 지원합니다.

## 주요 기능

*   **사용자 관리:** 회원가입 및 사용자 정보 조회
*   **표준 인증:** 이메일과 비밀번호를 사용한 JWT 토큰 기반 인증
*   **Google OAuth 2.0:** 구글 계정을 이용한 간편 로그인 TODO
*   **비밀번호 보안:** `passlib`와 `bcrypt`를 사용한 안전한 비밀번호 해싱
*   **데이터베이스:** `SQLAlchemy` ORM을 통한 비동기 `SQLite` 데이터베이스 연동
*   **API 문서:** `Swagger UI`를 통한 자동 대화형 API 문서 제공
*   **환경 변수 관리:** `Pydantic`을 사용한 안전한 설정 관리

## 프로젝트 구조

```
/
├── .env                 # 환경 변수 파일
├── .env.example         # 환경 변수 예시 파일
├── requirements.txt     # 프로젝트 의존성 목록
├── README.md            # 프로젝트 설명 파일
├── sso.db               # SQLite 데이터베이스 파일
└── src/
    ├── __init__.py
    ├── main.py          # FastAPI 앱 진입점 및 API 라우터
    ├── api/
    │   ├── __init__.py
    │   └── auth.py      # 인증 관련 로직 (JWT, OAuth2)
    ├── core/
    │   ├── __init__.py
    │   └── config.py    # 환경 변수 로드 및 설정
    ├── db/
    │   ├── __init__.py
    │   ├── database.py  # 데이터베이스 연결 및 세션 관리
    │   ├── models.py    # SQLAlchemy 데이터베이스 모델
    │   └── crud.py      # 데이터베이스 CRUD 작업
    └── schemas/
        ├── __init__.py
        └── schemas.py   # Pydantic 데이터 스키마
```

## 설치 및 실행 방법

### 1. 사전 요구사항

*   Python 3.8 이상
*   Google Cloud Platform 계정 및 OAuth 2.0 클라이언트 ID (구글 로그인 기능 사용 시)

### 2. 프로젝트 설정

1.  **저장소 복제 (선택 사항):**
    ```bash
    git clone <repository-url>
    cd sso
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate    # Windows
    ```

3.  **필요한 라이브러리 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **환경 변수 설정:**
    *   `.env.example` 파일을 `.env`로 복사합니다.
    *   `.env` 파일을 열고 `JWT_SECRET_KEY`에 강력한 비밀 문자열을 설정합니다.
    *   구글 로그인 기능을 활성화하려면, Google Cloud Console에서 생성한 OAuth 2.0 클라이언트 정보를 `.env` 파일에 기입합니다.
        *   **주의:** Google Cloud OAuth 클라이언트 설정 시 "승인된 리디렉션 URI"에 `http://localhost:8000/auth/google/callback`을 반드시 추가해야 합니다.

    ```.env
    # GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
    # GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"
    JWT_SECRET_KEY="YOUR_SUPER_SECRET_KEY"
    ```

### 3. 애플리케이션 실행

아래 명령어를 사용하여 FastAPI 개발 서버를 시작합니다.

```bash
uvicorn src.main:app --reload
```

서버가 성공적으로 실행되면, 터미널에 `Uvicorn running on http://127.0.0.1:8000` 메시지가 표시됩니다.

## API 테스트 (Swagger UI)

웹 브라우저에서 `http://localhost:8000/docs`로 접속하여 대화형 API 문서를 확인하고 모든 엔드포인트를 직접 테스트할 수 있습니다.

1.  **회원가입 (`POST /auth/register`):**
    *   `email`, `password`, `full_name`을 JSON 형식으로 입력하여 새 사용자를 등록합니다.

2.  **일반 로그인 (`POST /auth/token`):**
    *   `application/x-www-form-urlencoded` 형식으로 `username`(이메일)과 `password`를 전송하여 JWT 액세스 토큰을 발급받습니다.

3.  **구글 로그인 (`GET /auth/google/login`):**
    *   (현재 주석 처리됨) 엔드포인트를 실행하면 구글 로그인 페이지로 이동합니다.
    *   로그인 및 권한 동의 후, 설정된 콜백 URL(`http://localhost:8000/auth/google/callback`)로 리디렉션되며 응답으로 JWT 액세스 토큰을 받습니다.

4.  **보호된 엔드포인트 (`GET /users/me`, `GET /users`):**
    *   Swagger UI 우측 상단의 `Authorize` 버튼을 클릭합니다.
    *   Value 입력창에 `Bearer <YOUR_ACCESS_TOKEN>` 형식으로 토큰을 입력하고 `Authorize` 버튼을 누릅니다.
    *   이제 자물쇠가 잠긴 엔드포인트를 테스트할 수 있습니다. `/users/me`를 실행하면 현재 인증된 사용자의 정보를 반환하고, `/users`를 실행하면 사용자 목록을 반환합니다.