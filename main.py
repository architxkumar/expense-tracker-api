from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI, Depends, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from db.database import get_session, engine
from dto.user import UserCreate
from middleware.cross_origin_resource_sharing_middleware import cross_origin_resource_sharing_middleware
from middleware.error_handler_middleware import error_handler_middleware
from middleware.logger_middleware import logger_middleware
from middleware.request_id_middleware import request_id_middleware
from middleware.security_middleware import security_middleware
from service.user_service import UserService

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
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


@app.post("/signup")
async def signup(data: UserCreate, session: AsyncSession = Depends(get_session)):
    service = UserService(session)
    try:
        await service.create_user(data)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"})
