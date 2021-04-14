from fastapi.requests import Request
from fastapi.responses import JSONResponse

from ancillaries_ski.exceptions import ClientError


async def client_error_handler(request: Request, exc: ClientError) -> JSONResponse:
    content = {
        'error': exc.json()
    }

    return JSONResponse(
        status_code=400,
        content=content,
    )
