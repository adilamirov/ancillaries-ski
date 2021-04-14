from fastapi.requests import Request

from ancillaries_ski.client import Client


def get_client(request: Request) -> Client:
    return request.app.state.client
