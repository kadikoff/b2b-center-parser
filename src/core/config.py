from pathlib import Path
from typing import ClassVar, Type

from fastapi.openapi.models import Response
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Путь до корневой папки проекта
BASE_PROJECT_DIR = Path(__file__).parent.parent.parent  # /b2b-center-parser


API_DOCS_TITLE = "B2b center parser"
API_DOCS_DESCRIPTION = (
    "API-документация для сервиса по парсингу тендеров "
    "с сайта https://www.b2b-center.ru/market/"
)


class FastApiConfig(BaseModel):
    """Настройки для приложения FastAPI"""

    default_response_class: ClassVar[Type[Response]] = ORJSONResponse
    docs_title: str = API_DOCS_TITLE
    docs_description: str = API_DOCS_DESCRIPTION


class RunConfig(BaseModel):
    """Настройки для Uvicorn"""

    host: str = "localhost"
    port: int = 8000
    app: str = "run_app:app"
    reload: bool = True


class Settings(BaseSettings):
    """Корневая конфигурация приложения"""

    api: FastApiConfig = FastApiConfig()
    run: RunConfig = RunConfig()


settings = Settings()
