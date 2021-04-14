from typing import Callable

from fastapi import FastAPI

from ancillaries_ski import settings
from ancillaries_ski.client import Client


def start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        app.state.client = Client(settings.HOST)

    return start_app


def stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await app.state.client.close()

    return stop_app
