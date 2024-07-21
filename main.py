from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.database import create_tables
from apps.routes import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title='task management service'
)
app.include_router(router=task_router)
