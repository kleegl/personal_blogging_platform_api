from sqlalchemy import Column, ForeignKey, Integer, Unicode, DateTime
from sqlalchemy.orm import Relationship
from datetime import datetime, UTC

from core import Base


class PostTag(Base):
    __tablename__ = "post_tags"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128), unique=True, nullable=False)
    posts = Relationship("Post", secondary="post_tags", back_populates="tags")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(256), unique=True, nullable=False)
    content = Column(Unicode, nullable=False)
    created_at = Column(DateTime(timezone=True), insert_default=datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        insert_default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
    tags = Relationship("Tag", secondary="post_tags", back_populates="posts")
