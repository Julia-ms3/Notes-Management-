from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class NoteModel(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str]
    description: Mapped[str]
