#!/bin/bash
# 프로젝트 루트 디렉토리를 워킹 디렉토리로 설정하고 테스트 실행
PYTHONPATH=. pytest "$@"
