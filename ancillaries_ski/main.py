from fastapi import FastAPI

from ancillaries_ski.events import start_app_handler, stop_app_handler
from ancillaries_ski.exception_handlers import client_error_handler
from ancillaries_ski.exceptions import ClientError
from ancillaries_ski.routes import router


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler('startup', start_app_handler(application))
    application.add_event_handler('shutdown', stop_app_handler(application))

    application.add_exception_handler(ClientError, client_error_handler)

    application.include_router(router)

    return application


app = get_application()
