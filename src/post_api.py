from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models import Post, Tag
from schema import (
    PostCreateSchema,
    PostQuery,
    PostResponse,
    PostUpdateSchema,
    TagResponse,
)

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_db


post_router = APIRouter(prefix="/posts", tags=["/post"])


@post_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def create(
    post_create: PostCreateSchema, session: AsyncSession = Depends(get_db)
):
    db_tags = []
    for tag in post_create.tags:
        query = select(Tag).where(Tag.name == tag.name)
        result = await session.execute(query)
        db_tag = result.scalar_one_or_none()
        if db_tag is None:
            db_tag = Tag(name=tag.name)
            session.add(db_tag)
            await session.flush()
        db_tags.append(db_tag)
    post_data = post_create.model_dump()
    post_data.pop("tags", None)
    model = Post(**post_data)
    model.tags = db_tags
    session.add(model)
    await session.commit()
    await session.refresh(model)

    query = select(Post).where(Post.id == model.id).options(selectinload(Post.tags))
    result = await session.execute(query)
    post = result.scalar_one()

    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        updated_at=post.updated_at,
        tags=[TagResponse(id=tag.id, name=tag.name) for tag in post.tags],
    )


@post_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db)):
    post = await session.get(Post, id, options=[selectinload(Post.tags)])
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )
    return post


@post_router.put("/update", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def update(
    id: int, post_update: PostUpdateSchema, session: AsyncSession = Depends(get_db)
):
    post = await session.get(Post, id, options=[selectinload(Post.tags)])
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )

    tags_from_db = []
    if post_update.tags is not None:
        for tag in post_update.tags:
            query = select(Tag).where(Tag.name == tag.name)
            result = await session.execute(query)
            db_tag = result.scalar_one()
            if db_tag is None:
                db_tag = Tag(name=tag.name)
                session.add(db_tag)
                await session.flush()
            tags_from_db.append(db_tag)

        post.tags = tags_from_db
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    await session.commit()
    await session.refresh(post)
    return post


@post_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    post = await session.get(Post, id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )
    await session.delete(post)
    return status.HTTP_200_OK


@post_router.post(
    "/", status_code=status.HTTP_200_OK, response_model=List[PostResponse]
)
async def get_by_query(query: PostQuery, session: AsyncSession = Depends(get_db)):
    stmt = select(Post).options(selectinload(Post.tags))

    if query.date_to:
        stmt = stmt.where(Post.created_at < query.date_to)
    if query.date_from:
        stmt = stmt.where(Post.created_at > query.date_from)
    if query.tags and len(query.tags) != 0:
        stmt = stmt.where(Post.tags.any(Tag.name.in_([tag.name for tag in query.tags])))

    print(stmt)
    result = await session.execute(stmt)
    posts = result.scalars().all()

    return posts
