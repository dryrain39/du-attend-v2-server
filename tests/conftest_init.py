import pytest
import sys
import os
import importlib
from unittest.mock import patch, MagicMock

# 환경 변수로 테스트 실행 여부를 설정
os.environ["TESTING"] = "1"

# 필요한 모듈들을 미리 import하기 전에 패치
with patch('sqlalchemy.create_engine'):
    # 이제 main.py를 import하면 create_engine이 패치된 상태로 실행됨
    if "main" in sys.modules:
        importlib.reload(sys.modules["main"])
    else:
        import main
