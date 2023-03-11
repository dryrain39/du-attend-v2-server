import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_version():
    version = "230312"
    try:
        node = os.uname().nodename
    except:
        node = "unknown"

    node_name = os.getenv("NODE_NAME", "unknown")
    if node_name:
        node = node_name

    return {
        "version": version,
        "node": node,
        "version_string": f"서버: {node}<br>버전: {version}_최종_진짜최종.git"
    }
