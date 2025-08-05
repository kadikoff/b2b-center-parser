from fastapi import FastAPI
import uvicorn

from api.routes import router
from core.config import settings

app = FastAPI(
    default_response_class=settings.api.default_response_class,
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
