from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .model_base import Base


class Tenders(Base):
    __tablename__ = "tenders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    tender_id: Mapped[str] = mapped_column(String(50), nullable=False)  # "№"
    organizer: Mapped[str] = mapped_column(String(255), nullable=True)  # "Организатор"
    url: Mapped[str] = mapped_column(Text, nullable=False)  # "Ссылка на тендер"
    description: Mapped[str] = mapped_column(Text, nullable=True)  # "Описание"
    end_date: Mapped[str] = mapped_column(String(50), nullable=True)  # "Дата окончания"

    def __repr__(self):
        return (
            f"Tenders(id={self.id}, tender_id={self.tender_id}, "
            f"organizer={self.organizer}, url={self.url}, "
            f"description={self.description}, end_date={self.end_date})"
        )
