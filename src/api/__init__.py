from fastapi import APIRouter

from src.api.routers.geminiAPI import router as ai_router
from src.api.routers.note_history import router as note_history_router
from src.api.routers.notes import router as note_router

root_router = APIRouter()
root_router.include_router(note_router)
root_router.include_router(note_history_router)
root_router.include_router(ai_router)
