import os

from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/{full_path:path}")
async def redirect():
    return RedirectResponse(
        '/',
        status_code=status.HTTP_307_TEMPORARY_REDIRECT)
