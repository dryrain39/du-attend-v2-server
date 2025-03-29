# SQLite 스레드 간 연결 사용 문제

## 문제 상황

FastAPI 애플리케이션에서 SQLite 데이터베이스를 사용할 때 다음과 같은 오류가 발생했습니다:

```
sqlalchemy.exc.ProgrammingError: (sqlite3.ProgrammingError) SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 75460 and this is thread id 49064.
```

SQLite는 기본적으로 스레드 세이프하지 않으며, 연결이 생성된 스레드에서만 사용할 수 있습니다. 비동기 웹 애플리케이션에서는 여러 스레드가 생성되어 이런 문제가 발생할 수 있습니다.

## 해결 방법

### 1. check_same_thread=False 파라미터 추가

SQLite URL에 `check_same_thread=False` 파라미터를 추가하여 다른 스레드에서도 연결을 사용할 수 있게 합니다:

```python
SQLITE_URL = "sqlite:///C:/Users/~/PycharmProjects/du-attend-v2-server/user_db/test_serv_db.sqlite?check_same_thread=False"
```

**주의사항**: 이 방법은 SQLite가 스레드 간 동시 접근에 대한 보호를 비활성화합니다. 따라서 데이터 일관성을 위한 추가적인 락 메커니즘을 고려해야 합니다.

### 2. 연결 풀 설정 변경

SQLAlchemy의 연결 풀 설정을 변경하여 매 요청마다 새로운 연결을 생성하도록 합니다:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

engine = create_engine(
    "sqlite:///C:/Users/~/PycharmProjects/du-attend-v2-server/user_db/test_serv_db.sqlite",
    poolclass=NullPool
)
```

### 3. 세션 관리 최적화

FastAPI의 의존성 주입 시스템에서 세션이 적절히 관리되는지 확인합니다:

```python
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

모든 데이터베이스 작업이 동일한 요청 처리 스레드 내에서 완료되도록 해야 합니다.

## 권장 사항

개발 환경에서는 `check_same_thread=False` 옵션을 사용하는 것이 가장 간단한 해결책이지만, 프로덕션 환경에서는 SQLite보다 PostgreSQL이나 CockroachDB와 같은 완전한 클라이언트-서버 데이터베이스를 사용하는 것이 더 적합할 수 있습니다.

## 참고 자료

- SQLAlchemy 공식 문서: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#threading-pooling-behavior
- SQLite 스레딩 모델: https://www.sqlite.org/threadsafe.html
