import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager

from ancillaries_ski.client import Client


@pytest.fixture
def app() -> FastAPI:
    from ancillaries_ski.main import get_application

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
def client(initialized_app: FastAPI) -> Client:
    return initialized_app.state.client

