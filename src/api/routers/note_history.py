from fastapi import APIRouter
from sqlalchemy import select

from src.api.dependencies import SessionDepends
from src.database import Base, engine
from src.models import NoteHistoryModel

router = APIRouter(tags=["NOTES HISTORY"])


@router.post('/init_db_history')
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'configured': True}


@router.get("/get_history")
async def get_history(session: SessionDepends):
    query = select(NoteHistoryModel)
    result = await session.execute(query)
    return result.scalars().all()
