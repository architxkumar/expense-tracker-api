from logging.config import dictConfig

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import Response

from middleware.cross_origin_resource_sharing_middleware import cross_origin_resource_sharing_middleware
from middleware.error_handler_middleware import error_handler_middleware
from middleware.logger_middleware import logger_middleware
from middleware.request_id_middleware import request_id_middleware
from middleware.security_middleware import security_middleware

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "uvicorn": {"level": "ERROR"},
        "uvicorn.error": {"level": "ERROR"},
        "uvicorn.access": {"level": "CRITICAL"},
    }
})

limiter = Limiter(key_func=get_remote_address, headers_enabled=True)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



app.middleware("http")(cross_origin_resource_sharing_middleware)
app.middleware("http")(security_middleware)
app.middleware("http")(error_handler_middleware)
app.middleware("http")(logger_middleware)
app.middleware("http")(request_id_middleware)


@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request, response: Response):
    return {"message": "Hello World"}


@app.get("/hello/{name}")

async def say_hello(name: str):
    return {"message": f"Hello {name}"}
