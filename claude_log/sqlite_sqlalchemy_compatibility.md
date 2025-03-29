# SQLite와 SQLAlchemy 호환성 문제 기록

## 문제점
테스트 환경에서 SQLite를 사용할 때 다음과 같은 오류 발생:
```
sqlite3.OperationalError: near "ON": syntax error
CREATE TABLE users (
    id INTEGER NOT NULL, 
    username VARCHAR, 
    password VARCHAR, 
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL, 
    attend_data TEXT, 
    PRIMARY KEY (id)
)
```

## 원인
- SQLite는 `ON UPDATE CURRENT_TIMESTAMP` 구문을 지원하지 않음
- 이 구문은 MySQL/MariaDB에서는 정상 작동함
- 실제 프로덕션에서는 CockroachDB를 사용하고 있으나 테스트는 SQLite 사용

## 해결 방법
1. SQLAlchemy의 `onupdate` 기능 활용:
```python
from sqlalchemy import func

class TimestampMixin:
    @declared_attr
    def updated_time(cls):
        return Column(TIMESTAMP, nullable=False, 
                      server_default=text('CURRENT_TIMESTAMP'),
                      onupdate=func.current_timestamp())
```

2. User 및 Log 엔티티 모델에서 해당 믹스인 사용:
```python
class User(Base, TimestampMixin):
    __tablename__ = "users"
    # ...
```

## 주의사항
- 테스트 환경과 프로덕션 환경 간의 데이터베이스 차이로 인한 호환성 문제 발생 가능
- SQLite 특화 문법이나 CockroachDB 특화 문법을 피하고 공통 기능만 사용하는 것이 중요
- 필요한 경우 데이터베이스 방언(dialect)에 따라 다른 구현을 제공하는 추상화 설계 고려
