import os

from fastapi import APIRouter, Depends
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse

from enums.logtype import LogType
from schemas.log_schemas import LogInsert
from service.log_service import LogInsertService

router = APIRouter()


@router.get("/{full_path:path}")
async def redirect(background_tasks: BackgroundTasks, full_path: str,
                   log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.REDIRECT, attr=f"{full_path}"))

    return RedirectResponse(
        '/',
        status_code=status.HTTP_307_TEMPORARY_REDIRECT)
