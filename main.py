import logging
from urllib.request import Request

import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from route.router import api_router
from settings import SENTRY_DSN, SENTRY_ENV, SENTRY_TRACES_SAMPLE_RATE

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=SENTRY_ENV,
    traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    # integrations=[
    #     RedisIntegration(),
    # ],
)

app = FastAPI()

origins = [
    "http://dryrain39.github.io",
    "https://dryrain39.github.io",
    "http://kpc",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    app.add_middleware(SentryAsgiMiddleware)
except Exception as e:
    logging.error("SENTRY INIT FAILED.", exc_info=True)
    pass

# 라우터 추가
app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/7qy38tiejfkdnojiwgu9eyhijdfk")
async def server_checker():
    return {"message": "Hello World"}


@app.get("/")
async def root():
    return RedirectResponse(url='/static/index.html')
