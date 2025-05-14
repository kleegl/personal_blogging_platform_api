from fastapi import APIRouter, Depends
from models import Post
from schema import PostSchema

from sqlalchemy.ext.asyncio import AsyncSession

from core import get_db


post_router = APIRouter(tags=["/post"])


@post_router.post("/create")
async def create(post_create: PostSchema, session: AsyncSession = Depends(get_db)):
    model = Post(**post_create.model_dump())
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model
