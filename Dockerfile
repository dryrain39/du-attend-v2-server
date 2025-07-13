# syntax=docker/dockerfile:1.7          # buildx 최신 기능 사용
FROM --platform=$BUILDPLATFORM ghcr.io/astral-sh/uv:python3.9-alpine AS builder

ENV UV_COMPILE_BYTECODE=1
# 바이트코드 미리 컴파일로 cold-start 단축
ENV UV_LINK_MODE=copy
# 하드링크 경고 제거

# ────────────────────────
# 1단계: 시스템 의존 패키지
# ────────────────────────
# psycopg2-binary 대신 psycopg      ➜ libpq 필요
RUN apk add --no-cache --virtual .build-deps \
        build-base musl-dev libffi-dev postgresql-dev

# ────────────────────────
# 2단계: Python 의존성
# ────────────────────────
WORKDIR /app

# 종속성만 먼저 복사 → 캐시 최적화
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project          \
            --locked                      \
            --compile-bytecode

# ────────────────────────
# 3단계: 애플리케이션 소스
# ────────────────────────
COPY . .
RUN uv sync --compile-bytecode            \
            --locked

# ────────────────────────
# 4단계: 실행 전용 이미지로 슬림화
# ────────────────────────
FROM ghcr.io/astral-sh/uv:python3.9-alpine AS runtime
WORKDIR /app
COPY --from=builder /app /app

# 불필요한 헤더·컴파일러 패키지 제거
RUN apk del --no-network .build-deps || true

# 권한 분리 (선택)
RUN adduser -D -u 10001 appuser
USER appuser

ENTRYPOINT ["uv", "run", "/app/entry.sh"]
