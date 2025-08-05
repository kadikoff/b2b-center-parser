from pydantic import BaseModel, Field


class BaseTenders(BaseModel):
    """Вложенная схема с данными о тендере"""

    id: int = Field(
        description="Уникальный идентификатор тендера в базе данных",
        examples=[1],
    )
    tender_id: int = Field(
        description="Номер тендера",
        examples=[4128950],
    )
    organizer: str = Field(
        description="Организатор тендера",
        examples=['ООО "АКБ-ЦЕНТР"'],
    )
    url: str = Field(
        description="Ссылка на тендер",
        examples=["https://www.b2b-center.ru/app/market-next/postavka-stroitelnykh-materialov-profnastil/tender-4128948/"],
    )
    description: str = Field(
        description="Описание тендера",
        examples=["Сервис весового оборудования"],
    )
    end_date: str = Field(
        description="Дата завершения тендера",
        examples=["08.08.2025 16:00"],
    )


class TendersRead(BaseModel):
    """Схема для ответа API при запросе данных о тендерах

    Используется в эндпоинте:
    - GET /tenders - получить данные о тендерах
    """

    tenders: list[BaseTenders] = Field(description="Список данных о тендерах")
