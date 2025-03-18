from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class NoteModel(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now(),
                                              onupdate=func.now())


class NoteHistoryModel(Base):
    __tablename__ = 'history_notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey('notes.id'))
    header: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    created: Mapped[datetime] = mapped_column(DateTime)
    updated: Mapped[datetime] = mapped_column(DateTime)
