from fastapi import FastAPI
from api import post_router

app = FastAPI()

app.include_router(post_router)


@app.get("/health_check")
async def get():
    return "success"
