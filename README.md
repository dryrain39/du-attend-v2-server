# DU Attend v2.1

DU Attend는 대구대 강의실에서 QR 코드 기반 전자출결을 더 편리하게 도와주는 웹 서비스입니다. 학생들이 강의실 벽면에 부착된 QR 코드를 미리 등록해두면, 이후에는 바로 출석 링크를 통해 출결을 할 수 있어 매번 QR 코드를 스캔할 필요가 없습니다.

## 주요 기능

- **강의실 QR 등록**: 일회성 QR 코드 스캔으로 강의실을 등록합니다.
- **빠른 출석 체크**: 등록된 강의실은 바로 출석 링크를 클릭하여 출결할 수 있습니다.
- **강의실 관리**: 강의실 이름 변경, 순서 변경, 삭제 기능을 제공합니다.
- **사용자 계정 관리**: 회원가입, 로그인, 비밀번호 변경 기능을 제공합니다.

## 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 프레임워크 사용
- **SQLAlchemy**: ORM을 통한 데이터베이스 관리
- **SQLite**: 개발 및 소규모 배포용 데이터베이스
- **DiskCache**: 캐시 관리 (TokenCache, QRCache)
- **Jinja2**: HTML 템플릿 렌더링
- **Sentry**: 에러 모니터링 및 로깅
- **Uvicorn**: ASGI 서버

### 프론트엔드
- **Bootstrap 5**: 반응형 UI 프레임워크
- **jQuery**: DOM 조작 및 AJAX 요청
- **Lucide**: 아이콘 라이브러리

### 인프라
- **Docker & Docker Compose**: 컨테이너화 및 배포

## 프로젝트 구조

```
du-attend-v2-server/
├── config/              # 환경 설정
├── database/            # 데이터베이스 연결 및 초기화
├── entity/              # 데이터베이스 모델
├── enums/               # 열거형 타입
├── route/               # API 라우터
│   ├── html/            # HTML 렌더링 
│   ├── misc/            # 기타 API
│   ├── qr/              # QR 관련 API
│   ├── user/            # 사용자 관리 API
│   └── router.py        # 메인 라우터
├── schemas/             # Pydantic 스키마
├── service/             # 비즈니스 로직
├── static/              # 정적 파일 (HTML, CSS, JS)
│   ├── fragment/        # HTML 조각 템플릿
│   ├── js/              # JavaScript 파일
│   └── css/             # CSS 파일
├── tests/               # 테스트 케이스
├── user_db/             # 사용자 데이터베이스
├── util/                # 유틸리티 함수
├── VO/                  # Value Objects
├── claude_log/          # Claude AI 협업 로그
├── Dockerfile           # Docker 이미지 빌드 정의
├── docker-compose.yml   # Docker Compose 서비스 정의
├── requirements.txt     # 패키지 의존성
└── main.py              # 애플리케이션 진입점
```

## 설치 및 실행 방법

### 로컬 개발 환경

1. 저장소 클론
   ```bash
   git clone https://github.com/dryrain39/du-attend-v2-server.git
   cd du-attend-v2-server
   ```

2. 가상환경 설정
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 구성 설정
   ```bash
   cp config/config.sample.py config/config.py
   # config.py 파일을 적절히 수정하세요
   ```

4. 서버 실행
   ```bash
   python main.py
   ```

5. 테스트 실행 (작업중)
   ```bash
   python run_tests.py
   # 또는
   pytest
   ```

### Docker를 이용한 배포

1. Docker 이미지 빌드 및 실행 (빌드 전 docker-compose.yml 파일내 build 항목을 활성화 해야 합니다)
   ```bash
   docker-compose up -d
   ```

## 개발자 및 기여자

DU Attend는 MiscThings 동아리에서 개발한 프로젝트입니다

