
from fastapi import FastAPI

from src.api import root_router

app = FastAPI()
app.include_router(root_router)
# if __name__ == '__main__':
#     uvicorn.run("src.main:app", reload=True)
