from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.api.dependencies import SessionDepends
from src.database import Base, engine
from src.models import NoteHistoryModel, NoteModel
from src.schemas import NoteAddSchema

router = APIRouter(tags=["NOTES"])


@router.post('/initialization')
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'configured': True}


@router.post('/new_note')
async def add_note(data: NoteAddSchema, session: SessionDepends):
    new_note = NoteModel(
        header=data.header,
        description=data.description,
    )
    session.add(new_note)
    await session.commit()
    return {"note added": True}


@router.get('/all_notes')
async def get_all_notes(session: SessionDepends):
    query = select(NoteModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get('/notes/{note_id}')
async def get_note(note_id: int, session: SessionDepends):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()
    if note is None:
        raise HTTPException(status_code=404, detail='this note not found')
    return note


@router.put('/notes/{note_id}')
async def update_note(note_id: int, session: SessionDepends, data: NoteAddSchema):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()

    add_history = NoteHistoryModel(
        note_id=note.id,
        header=note.header,
        description=note.description,
        created=note.created,
        updated=note.updated

    )
    session.add(add_history)

    if note is None:
        raise HTTPException(status_code=404, detail='this note not found')

    note.header = data.header
    note.description = data.description

    await session.commit()

    return note


@router.delete("/notes/{note_id}")
async def delete_note(note_id: int, session: SessionDepends):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()
    if note is None:
        raise HTTPException(status_code=404, detail='this note not found')

    await session.delete(note)
    await session.commit()

    return {'deleted': True}
