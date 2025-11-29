from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from db.database import get_session, engine
from dto.user import UserCreate, UserLogin
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.middleware("http")(security_middleware)
app.middleware("http")(logger_middleware)
app.middleware("http")(request_id_middleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


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


# FIX: Fastapi seems to be returning 422 instead of 400 for malformed requests
@app.post("/login")
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    service = UserService(session)
    try:
        jwt_token = await service.login_user(data)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": jwt_token})
