from fastapi import APIRouter
from sqlalchemy import select

from src.api.dependencies import SessionDepends
from src.api.services import summarize_text
from src.models import NoteModel

router = APIRouter(tags=["AI"])


@router.get("/summaryText/{note_id}")
async def summary_text(note_id: int, session: SessionDepends):
    query = select(NoteModel).filter_by(id=note_id)
    result = await session.execute(query)
    note = result.scalar()
    summary = summarize_text(note.description)
    return {"summary": summary}
