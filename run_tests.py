#!/usr/bin/env python
import os
import sys
import pytest
import warnings
from sqlalchemy.exc import SAWarning

if __name__ == "__main__":
    # 프로젝트 루트 디렉토리를 Python 경로에 추가
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # SQLAlchemy 경고 무시 설정
    warnings.filterwarnings("ignore", category=SAWarning)
    
    # SQLite 관련 경고 필터링
    warnings.filterwarnings("ignore", message=".*ON UPDATE.*")
    
    # 테스트 실행 (모든 명령줄 인수 전달)
    args = ["-v"]
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    
    sys.exit(pytest.main(args))
