from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///notes.db', echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDepends = Annotated[AsyncSession, Depends(get_session)]


class NoteAddSchema(BaseModel):
    header: str
    description: str


class Note(NoteAddSchema):
    id: int


class Base(DeclarativeBase):
    pass


class NoteModel(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str]
    description: Mapped[str]


@app.post('/initialization')
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'configured': True}


@app.post('/new_note')
async def add_note(data: NoteAddSchema, session: SessionDepends):
    new_note = NoteModel(
        header=data.header,
        description=data.description,
    )
    session.add(new_note)
    await session.commit()
    return {"note added": True}


@app.get('/all_notes')
async def get_all_notes(session: SessionDepends):
    query = select(NoteModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.get('/notes/{note_id}')
async def get_note(note_id: int, session: SessionDepends):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()
    if note is None:
        raise HTTPException(status_code=404, detail='this note not found')
    return note


@app.put('/notes/{note_id}')
async def update_note(note_id: int, session: SessionDepends, data: NoteAddSchema):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()

    if note is None:
        raise HTTPException(status_code=404, detail='this note not found')

    note.header = data.header
    note.description = data.description

    await session.commit()

    return note


@app.delete("/notes/{note_id}")
async def delete_not(note_id: int, session: SessionDepends):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()

    await session.delete(note)
    await session.commit()

    return {'deleted': True}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
