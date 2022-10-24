import os

from fastapi import APIRouter, Depends
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse

from enums.logtype import LogType
from schemas.log_schemas import LogInsert
from service.log_service import LogInsertService

router = APIRouter()


@router.get("/campaign/{campaign_name}/{full_path:path}")
async def redirect(background_tasks: BackgroundTasks, campaign_name: str, full_path: str,
                   log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert,
                              LogInsert(type=LogType.CAMPAIGN_CLICK, attr=f"{campaign_name}", sub_attr=f"{full_path}"))
    return RedirectResponse(
        full_path,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get("/menu/{campaign_name}/{full_path:path}")
async def redirect(background_tasks: BackgroundTasks, campaign_name: str, full_path: str,
                   log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert,
                              LogInsert(type=LogType.MENU_CLICK, attr=f"{campaign_name}", sub_attr=f"{full_path}"))
    return RedirectResponse(
        full_path,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT)
