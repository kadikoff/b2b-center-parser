from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
import uvicorn

from api.routes import router
from core.config import settings
from src.core.models.db_helper import db_helper
from src.core.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """Контекстный менеджер жизненного цикла приложения FastAPI

    Выполняет:
    1. Инициализацию базы данных
    2. Корректное освобождение ресурсов БД при завершении
    """

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await db_helper.engine.dispose()


app = FastAPI(
    default_response_class=settings.api.default_response_class,
    lifespan=lifespan,
    title=settings.api.docs_title,
    description=settings.api.docs_description,
)

app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(
        host=settings.run.host,
        port=settings.run.port,
        app=settings.run.app,
        reload=settings.run.reload,
    )
