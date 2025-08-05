from typing import Sequence

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Tenders


async def get_tenders(session: AsyncSession) -> list[Tenders | None]:
    """Получение данных о тендерах из базы данных"""

    db_response: Result = await session.execute(select(Tenders))
    tenders: Sequence[Tenders] = db_response.unique().scalars().all()

    return list(tenders)
