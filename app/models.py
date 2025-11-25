from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    fb_id = Column(String(100), unique=True, index=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)          # renamed from 'text' for clarity
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Enrichment fields
    emotion = Column(String(50), default="neutral")
    tone = Column(String(50), default="reflective")
    tags = Column(Text, default="")                 # comma-separated tags
    idioms = Column(Text, default="")               # comma-separated idioms

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
