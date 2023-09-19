from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import connection_string
from database import sessionmanager
from session import router as session_router

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:1234",
]

sessionmanager.init(connection_string)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(title="Crypto Analysis API", lifespan=lifespan)

app.include_router(session_router, tags=["sessions"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
