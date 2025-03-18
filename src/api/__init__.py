from src.api.router import router as note_router

from fastapi import APIRouter

root_router = APIRouter()
root_router.include_router(note_router)
