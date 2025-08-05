from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud import crud_tenders
from src.core.models import db_helper
from src.core.schemas.schemas_tenders import TendersRead

router = APIRouter()


@router.get(
    "/tenders",
    status_code=status.HTTP_200_OK,
    response_model=TendersRead,
    summary="Получить данные о тендерах",
)
async def get_tenders(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить данные о тендерах

    1. Получение сессии для базы данных
    2. Запрос данных из бд
    """

    tenders = await crud_tenders.get_tenders(session=session)
    return {"tenders": tenders}
