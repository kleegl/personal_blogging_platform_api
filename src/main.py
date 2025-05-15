from fastapi import FastAPI, status
from post_api import post_router
from tag_api import tag_router

app = FastAPI()

app.include_router(post_router)
app.include_router(tag_router)


@app.get("/health")
async def get_health():
    return status.HTTP_200_OK
