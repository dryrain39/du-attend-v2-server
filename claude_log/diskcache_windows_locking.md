# Windows 환경에서 DiskCache 파일 잠금 문제

## 발생 상황
테스트 종료 시 다음과 같은 오류 발생:
```
PermissionError: [WinError 32] 다른 프로세스가 파일을 사용 중이기 때문에 프로세스가 액세스 할 수 없습니다: 'C:\\Users\\~\\AppData\\Local\\Temp\\tmpjq4265en\\005\\cache.db'
```

## 원인
- Windows 환경에서 파일 핸들이 완전히 닫히기 전에 삭제를 시도할 때 발생
- DiskCache 라이브러리가 SQLite 연결을 내부적으로 사용하며, 모든 연결이 즉시 닫히지 않음
- Python의 가비지 컬렉션 시점과 OS의 파일 핸들 해제 시점 사이의 불일치

## 해결 방법

### 1. 예외 처리를 통한 방법
```python
# 테스트 후 정리
token_cache.close()
try:
    shutil.rmtree(temp_dir)
except PermissionError:
    print(f"Warning: Could not delete temporary directory {temp_dir}")
```

### 2. GC 강제 실행과 지연 추가
```python
import gc
import time

# 테스트 후 정리
token_cache.close()
time.sleep(0.1)  # 짧은 지연 시간 추가
gc.collect()     # 명시적 가비지 컬렉션

try:
    shutil.rmtree(temp_dir)
except PermissionError:
    print(f"Could not remove temporary directory: {temp_dir}")
```

### 3. 파일 삭제 재시도 로직
```python
def safe_rmtree(path, max_retries=5, retry_delay=0.5):
    for i in range(max_retries):
        try:
            shutil.rmtree(path)
            break
        except PermissionError:
            if i == max_retries - 1:
                # 최대 재시도 횟수 도달, 경고만 출력
                print(f"Warning: Could not remove {path} after {max_retries} attempts")
            else:
                # 잠시 대기 후 재시도
                time.sleep(retry_delay)
```

### 4. 다른 패키지 활용
- `send2trash` 패키지: 휴지통으로 파일 이동 (파일 잠금 상태에서도 가능)
- `pytest-tempdir`: 테스트 세션 종료 후 일괄 정리 지원

## 결론
테스트 함수 자체는 올바르게 실행되며, 임시 파일 정리 단계의 오류는 테스트 결과에 영향을 미치지 않음. 실용적인 접근법은 예외 처리를 추가하고 필요에 따라 간단한 지연 메커니즘을 사용하는 것입니다.
