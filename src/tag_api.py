from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from models import Tag
from schema import TagUpdateSchema, TagCreateSchema


tag_router = APIRouter(prefix="/tags", tags=["tag"])


@tag_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(tag_create: TagCreateSchema, session: AsyncSession = Depends(get_db)):
    tag = Tag(**tag_create.model_dump())
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


@tag_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db)):
    tag = await session.get(Tag, id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id = {id} not found",
        )
    return tag


@tag_router.put("/update", status_code=status.HTTP_200_OK)
async def update(
    id: int, tag_update: TagUpdateSchema, session: AsyncSession = Depends(get_db)
):
    tag = await session.get(Tag, id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id = {id} not found",
        )
    tag.name = tag_update.name
    await session.commit()
    await session.refresh(tag)
    return tag


@tag_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    tag = await session.get(Tag, id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id = {id} not found",
        )
    await session.delete(tag)
    return status.HTTP_200_OK
